from django import forms

from order.models import Printer


def _get_available_point():
    choose_printer_point = set()

    printers = Printer.objects.all()
    if printers:
        for printer in printers:
            choose_printer_point.add((printer.point_id, printer.name_printer))
        return choose_printer_point
    else:
        choose_printer_point.add((1, 'Не мае доступних для замовлення'))
        return choose_printer_point


class OrderForm(forms.Form):
    first_dish = forms.CharField(max_length=1000, label='Перша страва')
    second_dish = forms.CharField(max_length=1000, label='Друга страва')
    drinks = forms.CharField(max_length=1000, label='Напої')
    other = forms.CharField(max_length=1000, label='Інше')
    order_point = forms.ChoiceField(choices=_get_available_point(), label='Доступні точки замовлення')
