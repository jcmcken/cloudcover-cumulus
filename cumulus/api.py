from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from cumulus.models import Host, Key, Datum
from cumulus.paginator import CumulusPaginator
from cumulus.authentication import RemoteUserAuthentication
from cumulus.authorization import HostAuthorization, KeyAuthorization, DataAuthorization

class HostResource(ModelResource):
    class Meta:
        queryset = Host.objects.all()
        resource_name = 'host'
        authorization = HostAuthorization()
        authentication = RemoteUserAuthentication()
        paginator_class = CumulusPaginator

class KeyResource(ModelResource):
    class Meta:
        queryset = Key.objects.all()
        resource_name = 'key'
        authorization = KeyAuthorization()
        authentication = RemoteUserAuthentication()
        paginator_class = CumulusPaginator

class DatumResource(ModelResource):
    host = fields.ForeignKey(HostResource, 'host')
    key = fields.ForeignKey(KeyResource, 'key')

    class Meta:
        queryset = Datum.objects.all()
        resource_name = 'data'
        authorization = DataAuthorization()
        authentication = RemoteUserAuthentication()
        paginator_class = CumulusPaginator
