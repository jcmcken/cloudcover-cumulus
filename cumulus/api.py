from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.api import Api
from tastypie.validation import FormValidation
from cumulus.models import Host, Key, Datum
from cumulus.paginator import CumulusPaginator
from cumulus.authentication import RemoteUserAuthentication
from cumulus.authorization import HostAuthorization, KeyAuthorization, DataAuthorization
from cumulus.forms import HostForm, KeyForm, DatumForm
from cumulus.validation import ModelFormValidation

VERSION = 1


class CumulusResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        """
        Hack to get around ``https://github.com/toastdriven/django-tastypie/issues/854``
        """
        bundle.obj = self._meta.object_class()

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)
        self.authorized_create_detail(self.get_object_list(bundle.request), bundle)
        return self.save(bundle)

class HostResource(CumulusResource):
    class Meta:
        queryset = Host.objects.all()
        resource_name = 'host'
        authorization = HostAuthorization()
        authentication = RemoteUserAuthentication()
        paginator_class = CumulusPaginator
        validation = ModelFormValidation(form_class=HostForm)

class KeyResource(CumulusResource):
    class Meta:
        queryset = Key.objects.all()
        resource_name = 'key'
        authorization = KeyAuthorization()
        authentication = RemoteUserAuthentication()
        paginator_class = CumulusPaginator
        validation = ModelFormValidation(form_class=KeyForm)

class DatumResource(ModelResource):
    host = fields.ForeignKey(HostResource, 'host')
    key = fields.ForeignKey(KeyResource, 'key')

    class Meta:
        queryset = Datum.objects.all()
        resource_name = 'data'
        authorization = DataAuthorization()
        authentication = RemoteUserAuthentication()
        paginator_class = CumulusPaginator
        validation = ModelFormValidation(form_class=DatumForm)

v1_api = Api(api_name='v%d' % VERSION)
v1_api.register(HostResource())
v1_api.register(KeyResource())
v1_api.register(DatumResource())

API = v1_api
