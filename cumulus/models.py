from django.db import models
from django.conf import settings
import logging

LOG = logging.getLogger(__name__)

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)

    class Meta:
        abstract = True

class Host(TimestampedModel):
    name = models.CharField(max_length=255, blank=False)
    ip = models.IPAddressField(blank=False)

    class Meta:
        unique_together = ('name', 'ip')

class Key(TimestampedModel):
    DATETIME = 'datetime'
    STRING = 'string'
    FLOAT = 'float'
    INTEGER = 'integer'
    BOOLEAN = 'boolean'
    TYPES = (
      (DATETIME, 'Datetime'),
      (STRING, 'String'),
      (FLOAT, 'Float'),
      (INTEGER, 'Integer'),
      (BOOLEAN, 'Boolean'),
    )

    name = models.CharField(max_length=32, blank=False)
    description = models.TextField(blank=False)
    type = models.CharField(max_length=8, choices=TYPES, blank=False)

class Datum(TimestampedModel):
    value = models.CharField(max_length=255, blank=False)
    key = models.ForeignKey(Key, blank=False)
    host = models.ForeignKey(Host, blank=False)

    class Meta:
        # each host can only have 1 of each key
        unique_together = ('host', 'key')

# fake, db-less user model
class User(object):
    def __init__(self, name=None, groups=[]):
        self.name = name
        self.groups = groups

    def __str__(self):
        return str(self.name)

    @property
    def is_staff(self):
        staff_groups = getattr(settings, 'CUMULUS_STAFF_GROUPS', [])
        staff_users = getattr(settings, 'CUMULUS_STAFF_USERS', [])
        return self.name in staff_users or \
            set(self.groups).intersection(set(staff_groups))
    
    @property
    def is_superuser(self):
        superuser_groups = getattr(settings, 'CUMULUS_SUPERUSER_GROUPS', [])
        superusers = getattr(settings, 'CUMULUS_SUPERUSERS', [])
        result = self.name in superusers or \
            set(self.groups).intersection(set(superuser_groups))
        return result 

    def is_anonymous(self):
        # webserver authenticates
        return bool(self.name)

    def is_authenticated(self):
        # webserver authenticates
        return not self.is_anonymous()
