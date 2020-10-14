import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Menu_Item(models.Model):
    item_name = models.CharField(max_length=200, default='')

class Order(models.Model):
    Items = models.ForeignKey(Menu_Item, on_delete=models.CASCADE, default='')
    customer_name = models.CharField(max_length=55)
    # pickup_time = models.DateTimeField('pickup_time')

    def __str__(self):
        return self.customer_name
