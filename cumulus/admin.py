from django.contrib import admin
from cumulus.models import Host, Key, Datum

class HostAdmin(admin.ModelAdmin):
    pass

class KeyAdmin(admin.ModelAdmin):
    pass

class DatumAdmin(admin.ModelAdmin):
    pass

admin.site.register(Host, HostAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(Datum, DatumAdmin)
