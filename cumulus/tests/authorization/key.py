from tastypie.test import ResourceTestCase
from cumulus.models import Host, Key, Datum
from django.conf import settings

class KeyAuthorizationTest(ResourceTestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        super(KeyAuthorizationTest, self).setUp()
        self.key = Key.objects.get(name='foo')
        self.url = '/api/v1/key/%d' % self.key.pk
        self.list_url = '/api/v1/key'
        self.superuser = 'admin'
        self.fakeuser = 'fakeuser'
        self.post_data = {
          'name': 'bacon',
          'description': 'Bacon is delicious',
        }
        settings.CUMULUS_SUPERUSERS = [self.superuser]

    def tearDown(self):
        settings.CUMULUS_SUPERUSERS = []

    # GET one, no user
    def test_get_unauthorized_no_user(self):
        self.assertHttpUnauthorized(
          self.api_client.get(self.url)
        )

    # GET one, any authed user
    def test_get_authorized_user(self):
        self.assertHttpOK(
          self.api_client.get(self.url, HTTP_REMOTE_USER=self.fakeuser)
        )
        self.assertHttpOK(
          self.api_client.get(self.url, HTTP_REMOTE_USER=self.superuser)
        )
    
    # GET many, no user
    def test_get_list_unauthorized_no_user(self):
        self.assertHttpUnauthorized(
          self.api_client.get(self.list_url)
        )

    # GET many, any authed user
    def test_get_list_authorized_user(self):
        fakeuser_result = self.api_client.get(self.list_url, HTTP_REMOTE_USER=self.fakeuser)
        self.assertHttpOK(fakeuser_result)
        self.assertTrue(bool(self.deserialize(fakeuser_result)))
        superuser_result = self.api_client.get(self.list_url, HTTP_REMOTE_USER=self.superuser)
        self.assertHttpOK(superuser_result)
        self.assertTrue(bool(self.deserialize(superuser_result)))

    def _post(self, **kwargs):
        return self.api_client.post(self.list_url, format='json', data=self.post_data,
            **kwargs)
    
    # POST one, no user
    def test_post_unauthorized_no_user(self):
        self.assertHttpUnauthorized(self._post())

    # POST one, unauthed user
    def test_post_unauthorized_user(self):
        self.assertHttpUnauthorized(
          self._post(HTTP_REMOTE_USER=self.fakeuser)
        )
   
    # POST one, superuser
    def test_superuser_post_authorized(self):
        self.assertHttpCreated(
          self._post(HTTP_REMOTE_USER=self.superuser)
        )
