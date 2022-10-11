from django.contrib import admin

from .models import Printer, Check


class PrinterAdmin(admin.ModelAdmin):
    list_display = ['id', 'api_key', 'check_type']

    actions = ['mark_as_kitchen', 'mark_as_client', 'mark_as_all']

    def mark_as_kitchen(self, request, queryset):
        queryset.update(check_type='k')

    def mark_as_client(self, request, queryset):
        queryset.update(check_type='c')

    def mark_as_all(self, request, queryset):
        queryset.update(check_type='a')

    mark_as_kitchen.shot_description = 'Change to status - Kitchen!'
    mark_as_client.shot_description = 'Change to status - Client!'
    mark_as_all.shot_description = 'Change to status - All!'


class CheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'printer_id', 'type', 'status']
    list_filter = ['printer_id', 'type', 'status']

    actions = ['mark_as_new', 'mark_as_rendered', 'mark_as_printed']

    def mark_as_new(self, request, queryset):
        queryset.update(status='n')

    def mark_as_rendered(self, request, queryset):
        queryset.update(status='r')

    def mark_as_printed(self, request, queryset):
        queryset.update(status='p')

    mark_as_new.shot_description = 'Change to status - New!'
    mark_as_rendered.shot_description = 'Change to status - Rendered!'
    mark_as_printed.shot_description = 'Change to status - Printed!'


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)
