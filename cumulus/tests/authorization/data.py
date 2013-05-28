"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from tastypie.test import ResourceTestCase
from cumulus.models import Host, Key, Datum
from django.conf import settings

class DataAuthorizationTest(ResourceTestCase):
    fixtures = ['test_single.json']

    def setUp(self):
        super(DataAuthorizationTest, self).setUp()
        self.server = 'localhost'
        self.host = Host.objects.get(name=self.server)
        self.datum = Datum.objects.get(host_id=self.host.pk)
        self.url = '/api/v1/data/%d' % self.datum.pk
        self.list_url = '/api/v1/data'
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
        self.assertHttpOK(
          self.api_client.get(self.list_url, HTTP_REMOTE_USER=self.server)
        )

    # GET many, superuser
    def test_superuser_get_list_authorized(self):
        result = self.api_client.get(self.list_url, HTTP_REMOTE_USER=self.superuser)
        self.assertHttpOK(result)
        data = self.deserialize(result)
        self.assertTrue(bool(data['objects']))
