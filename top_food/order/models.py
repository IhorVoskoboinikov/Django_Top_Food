from django.db import models


# Create your models here.

class Printer(models.Model):
    CHECK_TYPE_CHOICES = [
        ('Kitchen', 'Kitchen'),
        ('Client', 'Client'),
    ]
    name_printer = models.CharField(max_length=200, verbose_name='Назва принтеру')
    api_key = models.CharField(max_length=200)
    check_type = models.CharField(max_length=10, choices=CHECK_TYPE_CHOICES,
                                  verbose_name='тип чеку')
    point_id = models.IntegerField()

    class Meta:
        verbose_name = 'Принтер'
        verbose_name_plural = 'Принтери'

    def __str__(self):
        return f'{self.id}'


class Check(models.Model):
    STATUS_CHOICES = [
        ('n', 'New'),
        ('r', 'Rendered'),
        ('p', 'Printed'),
    ]
    CHECK_TYPE_CHOICES = [
        ('k', 'Kitchen'),
        ('c', 'Client'),
    ]
    printer_id = models.ForeignKey(Printer, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=50)
    type = models.CharField(max_length=1, choices=CHECK_TYPE_CHOICES, verbose_name='тип принтеру')
    order = models.JSONField(verbose_name='Заказ')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='n',
                              verbose_name='статус')
    pdf_file = models.FileField()

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return f'{self.id}, {self.type}'
