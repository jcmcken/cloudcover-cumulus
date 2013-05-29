from tastypie.test import ResourceTestCase
from cumulus.models import Host, Key, Datum
from django.conf import settings

class HostAuthorizationTest(ResourceTestCase):
    fixtures = ['fixtures.json']

    def setUp(self):
        super(HostAuthorizationTest, self).setUp()
        self.server = 'localhost'
        self.host = Host.objects.get(name=self.server)
        self.url = '/api/v1/host/%d' % self.host.pk
        self.list_url = '/api/v1/host'
        self.superuser = 'admin'
        self.fakeuser = 'fakeuser'
        settings.CUMULUS_SUPERUSERS = [self.superuser]

    def tearDown(self):
        settings.CUMULUS_SUPERUSERS = []

    # GET one, no user
    def test_get_unauthorized_no_user(self):
        self.assertHttpUnauthorized(
          self.api_client.get(self.url)
        )

    # GET one, unauthed user
    def test_get_unauthorized_user(self):
        self.assertHttpUnauthorized(
          self.api_client.get(self.url, HTTP_REMOTE_USER=self.fakeuser)
        )
   
    # GET one, authed user 
    def test_server_get_authorized(self):
        self.assertHttpOK(
          self.api_client.get(self.url, HTTP_REMOTE_USER=self.server)
        )

    # GET one, superuser
    def test_superuser_get_authorized(self):
        self.assertHttpOK(
          self.api_client.get(self.url, HTTP_REMOTE_USER=self.superuser)
        )
    
    # GET many, no user
    def test_get_list_unauthorized_no_user(self):
        self.assertHttpUnauthorized(
          self.api_client.get(self.list_url)
        )

    # GET many, unauthed user
    def test_get_list_unauthorized_user(self):
        result = self.api_client.get(self.list_url, HTTP_REMOTE_USER=self.fakeuser)
        self.assertHttpOK(result)
        data = self.deserialize(result)
        self.assertFalse(bool(data['objects']))
    
    # GET many, authed user
    def test_server_get_list_authorized(self):
        result = self.api_client.get(self.list_url, HTTP_REMOTE_USER=self.server)
        self.assertHttpOK(result)
        data = self.deserialize(result)
        self.assertTrue(len(data['objects']) == 1)

    # GET many, superuser
    def test_superuser_get_list_authorized(self):
        result = self.api_client.get(self.list_url, HTTP_REMOTE_USER=self.superuser)
        self.assertHttpOK(result)
        data = self.deserialize(result)
        self.assertTrue(len(data['objects']) == 2)
