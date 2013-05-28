from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.auth import get_user_model

class GroupEnabledRemoteUserBackend(RemoteUserBackend):
    def authenticate(self, remote_user, remote_groups):
        user = super(GroupEnabledRemoteUserBackend, self).authenticate(remote_user)
        user.remote_groups = remote_groups
        user.is_superuser = self._is_superuser(user)
        user.is_staff = self._is_staff(user)
        return user

    def _is_superuser(self, user): 
        superuser_groups = getattr(settings, 'CUMULUS_SUPERUSER_GROUPS', [])
        superusers = getattr(settings, 'CUMULUS_SUPERUSERS', [])
        result = user.username in superusers or \
            set(user.remote_groups).intersection(set(superuser_groups))
        return bool(result)
    
    def _is_staff(self, user):
        staff_groups = getattr(settings, 'CUMULUS_STAFF_GROUPS', [])
        staff_users = getattr(settings, 'CUMULUS_STAFF_USERS', [])
        result = user.username in staff_users or \
            set(user.remote_groups).intersection(set(staff_groups))
        return bool(result)
