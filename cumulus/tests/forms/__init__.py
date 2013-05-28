from tastypie.test import ResourceTestCase
from cumulus.models import Host, Key, Datum
from django.conf import settings

class ViolatesFormsTest(ResourceTestCase):
    def setUp(self):
        super(ViolatesFormsTest, self).setUp()
        self.server = 'localhost'
        self.host_url = '/api/v1/host'
        self.superuser = 'admin'
        settings.CUMULUS_SUPERUSERS = [self.superuser]

    def tearDown(self):
        settings.CUMULUS_SUPERUSERS = []

    def test_invalid_ip(self):
        result = self.api_client.post(self.host_url, format='json', 
            data={'ip':'foo','name':'bar'}, HTTP_REMOTE_USER=self.superuser)
        self.assertHttpBadRequest(result)
        data = self.deserialize(result)
        assert 'Enter a valid IP' in data['host']['ip'][0]
