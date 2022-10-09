from django.contrib import admin

from .models import Printer, Check


class PrinterAdmin(admin.ModelAdmin):
    pass


class CheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'printer_id', 'status']

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


admin.site.register(Printer)
admin.site.register(Check, CheckAdmin)
