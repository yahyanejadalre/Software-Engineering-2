from django.contrib import admin

from .models import DSO


@admin.register(DSO)
class DSOAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'price', 'name', 'is_available', 'active', 'created_at', 'updated_at')
    list_filter = ('is_available', 'active',)
    search_fields = ('identifier', 'name',)
    ordering = ('price', 'is_available', 'active', 'created_at', 'updated_at')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields.pop('identifier', None)
        return form
