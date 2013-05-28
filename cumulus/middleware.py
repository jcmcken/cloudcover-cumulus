from cumulus.models import User

class TrustedRemoteUserMiddleware(object):
    group_separator = '|'
    user_header = 'HTTP_REMOTE_USER'
    groups_header = 'HTTP_REMOTE_GROUPS'

    def process_request(self, request):
        name = request.META.get(self.user_header, None)
        groups_string = request.META.get(self.groups_header, None)
        if groups_string:
            groups = groups_string.split(self.group_separator)
        else:
            groups = []

        request.user = User(name=name, groups=groups)
