from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import load_backend
from django.conf import settings

class GroupEnabledRemoteUserMiddleware(RemoteUserMiddleware):
    header = 'HTTP_REMOTE_USER'
    groups_header = 'HTTP_REMOTE_GROUPS'
    group_separator = '|'

    def __init__(self):
        backends = getattr(settings, 'AUTHENTICATION_BACKENDS', [])
        if 'django.contrib.auth.backends.RemoteUserBackend' not in backends:
            raise ImproperlyConfigured(
                "The 'cumulus.backends.GroupEnabledRemoteUserBackend' backend requires "
                "the 'django.contrib.auth.backends.RemoteUserBackend' be loaded. Please "
                "alter your AUTHENTICATION_BACKENDS setting to suit.")

    def process_request(self, request):
        super(GroupEnabledRemoteUserMiddleware, self).process_request(request)
        if request.user:
            request.user = auth.authenticate(
                user=request.user, remote_groups=self._get_groups(request))

    def _get_groups(self, request):
        groups_string = request.META.get(self.groups_header, None)
        if groups_string:
            groups = groups_string.split(self.group_separator)
        else:
            groups = []
        return groups
