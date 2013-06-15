from django.contrib import admin
from cumulus.models import Host, Key, Datum

class DatumInline(admin.TabularInline):
    model = Datum

class HostAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated_at'
    list_display = ('id', 'name', 'ip', 'created_at', 'updated_at')
    ordering = ('-updated_at',)
    search_fields = ('name', 'ip')
    inlines = (DatumInline,)

class KeyAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated_at'
    list_display = ('id', 'name', 'created_at', 'updated_at')
    ordering = ('-updated_at',)
    search_fields = ('name',)

class DatumAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated_at'
    list_display = ('id', 'host', 'key', 'value', 'created_at', 'updated_at')
    list_display_links = ('value',)
    list_select_related = True
    ordering = ('-updated_at',)
    search_fields = ('value', 'host__name')

admin.site.register(Host, HostAdmin)
admin.site.register(Key, KeyAdmin)
admin.site.register(Datum, DatumAdmin)
