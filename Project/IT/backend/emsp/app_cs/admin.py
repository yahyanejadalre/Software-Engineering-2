from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from app_cs import models

# Register your models here.
app_name = 'app_cs'


@admin.register(models.ChargingSocket)
class ChargingSocketAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'type', 'station',)
    list_filter = ('type', 'station',)
    search_fields = ('identifier', 'type', 'station',)
    ordering = ('identifier', 'type', 'station',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields.pop('identifier', None)
        return form


class ChargingSocketInline(admin.TabularInline):
    model = models.ChargingSocket
    extra = 0


@admin.register(models.ChargingStation)
class ChargingStationAdmin(OSMGeoAdmin):
    list_display = ('location', 'power_source', 'price')
    list_filter = ('power_source', 'price')
    list_options = ('location', 'power_source', 'price')
    search_fields = ('location', 'power_source', 'price')

    inlines = [ChargingSocketInline]
