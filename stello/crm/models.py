from django.db import models


# Список клиентов
class Сustomer(models.Model):
    name = models.CharField(max_length=180, blank=True)
    account = models.CharField(max_length=180)
    phone_number = models.CharField(max_length=18, blank=True)

    class Meta:
        db_table = "customers"


# Список заказов
class Order(models.Model):
    customer = models.ForeignKey(
        Сustomer, related_name='customer_orders',
        on_delete=models.CASCADE)
    product = models.IntegerField()
    preview_text = models.CharField(max_length=180, blank=True)
    preview_file = models.FileField(
        upload_to='images', blank=True, null=True)
    material = models.IntegerField(null=True)
    classes = models.CharField(max_length=180, blank=True)
    count = models.IntegerField(default=1)

    class Meta:
        db_table = "orders"
