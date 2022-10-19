from django.contrib import admin

from .models import Printer, Check


class PrinterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_printer', 'api_key', 'check_type', 'point_id']

    actions = ['mark_as_kitchen', 'mark_as_client']

    def mark_as_kitchen(self, request, queryset):
        queryset.update(check_type='k')

    def mark_as_client(self, request, queryset):
        queryset.update(check_type='c')

    mark_as_kitchen.shot_description = 'Change to status - Kitchen!'
    mark_as_client.shot_description = 'Change to status - Client!'


class CheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'printer_id', 'type', 'status']
    list_filter = ['printer_id', 'type', 'status']

    actions = ['mark_as_new', 'mark_as_rendered', 'mark_as_printed']

    def mark_as_new(self, request, queryset):
        queryset.update(status='New')

    def mark_as_rendered(self, request, queryset):
        queryset.update(status='Rendered')

    def mark_as_printed(self, request, queryset):
        queryset.update(status='Printed')

    mark_as_new.shot_description = 'Change to status - New!'
    mark_as_rendered.shot_description = 'Change to status - Rendered!'
    mark_as_printed.shot_description = 'Change to status - Printed!'


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
