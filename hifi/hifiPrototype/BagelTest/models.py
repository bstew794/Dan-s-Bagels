import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class Order(models.Model):
    customer_name = models.CharField(max_length=50)
    pickup_time = models.DateTimeField('pickup_time')


    def __str__(self):
        return self.customer_name



class Menu_Item(models.Model):
    item_name = models.ForeignKey(Order, on_delete=models.CASCADE)
