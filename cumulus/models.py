from django.db import models
from django.conf import settings
from django.utils import timezone
from cumulus.defaults import INACTIVITY_MINIMUM
import datetime
import logging

LOG = logging.getLogger(__name__)

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=False,
        verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, blank=False,
        verbose_name='Last Updated')

    class Meta:
        abstract = True

    @property
    def is_active(self):
        inactivity = getattr(settings, 'CUMULUS_INACTIVITY_MINIMUM', INACTIVITY_MINIMUM)
        delta = datetime.timedelta(minutes=inactivity)
        return (timezone.now() - self.updated_at) <= delta

class Host(TimestampedModel):
    name = models.CharField(max_length=255, blank=False,
        verbose_name='Hostname')
    ip = models.IPAddressField(blank=False, verbose_name='IP Address')

    class Meta:
        unique_together = ('name', 'ip')

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.ip)

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

    name = models.CharField(max_length=32, blank=False, unique=True)
    description = models.TextField(blank=False)
    type = models.CharField(max_length=8, choices=TYPES, blank=False,
        verbose_name='Data Type')

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.type)

class Datum(TimestampedModel):
    value = models.CharField(max_length=255, blank=False)
    key = models.ForeignKey(Key, blank=False)
    host = models.ForeignKey(Host, blank=False)

    class Meta:
        # each host can only have 1 of each key
        unique_together = ('host', 'key')
        verbose_name_plural = 'data'

    def __unicode__(self):
        return "%s,%s=%s" % (self.host.name, self.key.name, self.value)
