from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth import load_backend

class GroupEnabledRemoteUserMiddleware(RemoteUserMiddleware):
    header = 'HTTP_REMOTE_USER'
    groups_header = 'HTTP_REMOTE_GROUPS'
    group_separator = '|'

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed. Edit your"
                " MIDDLEWARE_CLASSES setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            username = request.META[self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if request.user.is_authenticated():
                try:
                    stored_backend = load_backend(request.session.get(
                        auth.BACKEND_SESSION_KEY, ''))
                    if isinstance(stored_backend, RemoteUserBackend):
                        auth.logout(request)
                except ImproperlyConfigured as e:
                    # backend failed to load
                    auth.logout(request)
            return
        # If the user is already authenticated and that user is the user we are
        # getting passed in the headers, then the correct user is already
        # persisted in the session and we don't need to continue.
        if request.user.is_authenticated():
            if request.user.get_username() == self.clean_username(username, request):
                return
        # We are seeing this user for the first time in this session, attempt
        # to authenticate the user.
        groups = self._get_groups(request)
        user = auth.authenticate(remote_user=username, remote_groups=groups)
        if user:
            # User is valid. Set request.user and persist user in the session
            # by logging the user in.
            request.user = user
            auth.login(request, user)

    def _get_groups(self, request):
        groups_string = request.META.get(self.groups_header, None)
        if groups_string:
            groups = groups_string.split(self.group_separator)
        else:
            groups = []
        return groups
