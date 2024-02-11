from django.contrib import admin

from app_booking import models

# Register your models here.
app_name = 'app_booking'


@admin.register(models.BookingHistory)
class BookingHistoryAdmin(admin.ModelAdmin):
    list_display = ('status', 'charging_stared_at', 'start_time', 'end_time', 'unique_code', 'created_at')
    list_filter = ('status', 'start_time', 'end_time', 'created_at')
    search_fields = ('user', 'status', 'charging_socket', 'start_time', 'end_time', 'unique_code', 'created_at')
    ordering = ('status', 'charging_stared_at', 'start_time', 'end_time', 'created_at')

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields.pop('unique_code', None)
        form.base_fields.pop('created_at', None)
        return form

    # def get_queryset(self, request):
    #     return super().get_queryset(request).select_related('user', 'charging_socket', 'charging_socket__station')
