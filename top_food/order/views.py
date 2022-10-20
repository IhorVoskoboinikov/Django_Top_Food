import os
import re
from django.shortcuts import render
from django.views import View
from .models import Check, Printer
from .forms import OrderForm
import json
from fpdf import FPDF
from django.http import JsonResponse
from asgiref.sync import sync_to_async
import asyncio
import time


def create_pdf_check_async(order, order_number, order_point):
    printers = Printer.objects.filter(point_id=order_point)
    for printer in printers:
        pdf = FPDF(format='A5')
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'media/font/DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', '', 14)
        title = f'Ваше замовлення № {order_number}'
        pdf.cell(200, 10, txt=title, ln=1, align='L')
        for key, value in order.items():
            pdf.cell(200, 10, txt=f"{key} - {value}", ln=1, align='L')
        pdf.output(f'media/pdf/{order_number}_{printer.check_type}.pdf')
        print("---------The file is ready--------------")
        time.sleep(3)


def save_check_in_db_async(order_point, json_data, order_number):
    printers = Printer.objects.filter(point_id=order_point)
    for printer in printers:
        check_to_save = Check(
            printer_id=printer,
            api_key=printer.api_key,
            type=printer.check_type,
            order=json_data,
            pdf_file=f'{order_number}_{printer.check_type}.pdf',
            order_number=order_number
        )
        check_to_save.save()
        print("Save data in db")
        time.sleep(2)


def get_order_number():
    order_numbers = set()
    order_numbers_pattern = r'^[0-9]+'
    directory = 'media/pdf'
    files = os.listdir(directory)
    if not files:
        return 1
    for file in files:
        order = re.search(order_numbers_pattern, file)
        order_numbers.add(int(order.group()))
    order_numbers = max(order_numbers) + 1
    return order_numbers


def order_menu(request):
    order = OrderForm()
    return render(request, 'order.html', {'order': order})


async def order_is_accepted_async(request):
    start = time.time()
    order_dict = {
        'first_dish': request.POST['first_dish'],
        'second_dish': request.POST['second_dish'],
        'drinks': request.POST['drinks'],
        'other': request.POST['other'],
    }
    order_point = int(request.POST['order_point'])
    json_data = json.dumps(order_dict)
    order_number = get_order_number()
# asynco var#1
    loop = asyncio.get_event_loop()
    async_function1 = sync_to_async(save_check_in_db_async, thread_sensitive=False)
    async_function2 = sync_to_async(create_pdf_check_async, thread_sensitive=False)
    loop.create_task(async_function1(
        order_point=order_point,
        json_data=json_data,
        order_number=order_number))
    loop.create_task(async_function2(
        order=order_dict,
        order_number=order_number,
        order_point=order_point))
# asynco var#2 (decoration @sync_to_async to funk)
    # task1 = asyncio.ensure_future(save_check_in_db_async(
    #     order_point=order_point,
    #     json_data=json_data,
    #     order_number=order_number)
    # )
    # task2 = asyncio.ensure_future(create_pdf_check_async(
    #     order=order_dict,
    #     order_number=order_number,
    #     order_point=order_point)
    # )

    # await asyncio.wait([task1, task2])
    total_time = (time.time() - start)
    print(total_time)
    return render(request, 'form_done.html', {'order_dict': order_dict})


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
