from django.contrib import admin
from django.urls import path

from order import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.order_menu, name='order_menu'),
    path('order_is_accepted/', views.order_is_accepted_async, name='order_is_accepted'),
    path('get_files_for_printer/<int:printer_id>', views.PrinterView.as_view(), name='get_files_for_printer'),
]
