import os
import re
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Check, Printer
from .forms import OrderForm
import json
from fpdf import FPDF
from django.http import JsonResponse

import asyncio


def create_pdf_check(check, order):
    pdf = FPDF(format='A5')
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'media/font/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    title = f'Ваше замовлення № {check.order_number}'
    pdf.cell(200, 10, txt=title, ln=1, align='L')
    for key, value in order.items():
        pdf.cell(200, 10, txt=f"{key} - {value}", ln=1, align='L')
    pdf.output(f'media/pdf/{check.order_number}_{check.type}.pdf')


def get_order_number():
    order_numbers = set()
    order_numbers_pattern = r'^[0-9]+'
    directory = 'media/pdf'
    files = os.listdir(directory)
    if not files:
        return None
    for file in files:
        order = re.search(order_numbers_pattern, file)
        order_numbers.add(int(order.group()))
    order_numbers = max(order_numbers) + 1
    return order_numbers


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
    order_number = get_order_number()
    if not printers:
        return render(request, 'no_printer.html', {})
    for printer in printers:
        if printer.point_id == int(request.POST['order_point']):
            check_to_save = Check(
                printer_id=printer,
                api_key=printer.api_key,
                type=printer.check_type,
                order=json_data,
                pdf_file=f'{order_number}_{printer.check_type}.pdf',
                order_number=order_number
            )
            check_to_save.save()
            create_pdf_check(order=order_dict, check=check_to_save)
    return render(request, 'form_done.html', {'order_dict': order_dict})


def get_files_for_printer(request):
    checks = Check.objects.all()
    for check in checks:
        if check.status == 'Rendered':
            check.status = 'Printed'
            check.save()
    return render(request, 'get_files_for_printer.html')


class PrinterView(View):
    def get(self, request, printer_id):
        checks = Check.objects.filter(printer_id=printer_id, status='Rendered')
        checks_dict = {}
        if checks:
            for check in checks:
                check.status = 'Printed'
                check.save()
                with open(f'media/pdf/{check.pdf_file}', 'rb') as check_pdf:
                    pdf_str = check_pdf.read().decode('latin-1')
                    checks_dict[f'{check.pdf_file}'] = pdf_str
            return JsonResponse(checks_dict)
        else:
            return JsonResponse({'check': None})
