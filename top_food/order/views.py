import asyncio
import json
import time

from asgiref.sync import sync_to_async
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.db.models import Max
from fpdf import FPDF

from .models import Check, Printer
from .forms import OrderForm


def create_pdf_check_async(order, order_number, order_point):
    time.sleep(45)

    pdf = FPDF(format='A5')
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'media/font/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    title = f'Ваше замовлення № {order_number}'
    pdf.cell(200, 10, txt=title, ln=1, align='L')
    for key, value in order.items():
        pdf.cell(200, 10, txt=f"{key} - {value}", ln=1, align='L')

    printers = Printer.objects.filter(point_id=order_point)
    for check_type in set([i.check_type for i in printers]):
        pdf.output(f'media/pdf/{order_number}_{check_type}.pdf')

    print("---------The file is ready--------------")

    checks = Check.objects.filter(order_number=order_number)
    for check in checks:
        check.status = 'Rendered'
        check.save()

    print("========Checks is Rendered=========")


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


@sync_to_async
def get_order_number_async():

    order_number = Check.objects.aggregate(Max('order_number'))['order_number__max']
    if order_number:
        return order_number + 1
    return 1


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

    order_number = asyncio.create_task(get_order_number_async())
    await order_number

    loop = asyncio.get_event_loop()
    async_function1 = sync_to_async(save_check_in_db_async, thread_sensitive=False)
    async_function2 = sync_to_async(create_pdf_check_async, thread_sensitive=False)
    loop.create_task(async_function1(
        order_point=order_point,
        json_data=json_data,
        order_number=order_number.result()))
    loop.create_task(async_function2(
        order=order_dict,
        order_number=order_number.result(),
        order_point=order_point))

    total_time = (time.time() - start)
    print(total_time)

    return render(request, 'form_done.html', {
        'order_dict': order_dict,
        'order_number': order_number.result()
    })


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
