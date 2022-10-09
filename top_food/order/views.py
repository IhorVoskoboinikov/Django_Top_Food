from django.shortcuts import render
from .models import Check, Printer
from .forms import OrderForm
import json


# Create your views here.


def order_menu(request):
    order = OrderForm()
    return render(request, 'order.html', {'order': order})


def order_is_accepted(request):
    order_dict = {
        'first_dish': request.POST['first_dish'],
        'second_dish': request.POST['second_dish'],
        'drinks': request.POST['drinks'],
        'other': request.POST['other'],
    }
    json_data = json.dumps(order_dict)
    printers = Printer.objects.all()
    if printers:
        for printer in printers:
            check_to_save = Check(
                printer_id=printer,
                api_key=printer.api_key,
                type=printer.check_type,
                order=json_data,
            )
            check_to_save.save()
        return render(request, 'form_done.html', {'order_dict': order_dict})
    else:
        return render(request, 'no_printer.html', {})
