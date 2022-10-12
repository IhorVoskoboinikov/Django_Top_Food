from django.shortcuts import render
from .models import Check, Printer
from .forms import OrderForm
import json
from fpdf import FPDF


def create_pdf_check(check, order):
    pdf = FPDF(format='A5')
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'media/font/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    title = f'Ваше замовлення № {check.id}'
    pdf.cell(200, 10, txt=title, ln=1, align='L')
    for key, value in order.items():
        pdf.cell(200, 10, txt=f"{key} - {value}", ln=1, align='L')
    pdf.output(f'media/pdf/{check.id}_{check.type}.pdf')


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
            create_pdf_check(order=order_dict, check=check_to_save)
        return render(request, 'form_done.html', {'order_dict': order_dict})
    else:
        return render(request, 'no_printer.html', {})
