from tastypie.authentication import Authentication
import logging

LOG = logging.getLogger(__name__)

class RemoteUserAuthentication(Authentication):
    def get_identifier(self, request):
        return request.user.username

    def is_authenticated(self, request, **kwargs):
        # trust user passed from webserver, if there is one
        return bool(self.get_identifier(request))
