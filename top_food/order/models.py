from django.db import models


# Create your models here.

class Printer(models.Model):
    STATUS_CHOICES = [
        ('k', 'Kitchen'),
        ('c', 'Client'),
        ('all', 'Client/Kitchen'),
    ]
    name = models.CharField(max_length=200, verbose_name='Назва принтеру')
    api_key = models.CharField(max_length=200)
    check_type = models.CharField(max_length=1, choices=STATUS_CHOICES, default='all'),
    point_id = models.IntegerField()

    def __str__(self):
        return f'{self.name}'


class Check(models.Model):
    STATUS_CHOICES = [
        ('n', 'New'),
        ('r', 'Rendered'),
        ('p', 'Printed'),
    ]
    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    order = models.JSONField(verbose_name='Заказ')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n')
    pdf_file = models.FileField()

    def __str__(self):
        return f'{self.printer_id}, {self.status}'
