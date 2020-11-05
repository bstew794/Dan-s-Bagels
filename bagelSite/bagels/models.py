import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# An Order can only have one User but a User can have many Orders

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=50, default='')
    memberNumber = models.CharField(max_length=50, default='')
    cardNumber = models.CharField(max_length=50, default='')
    accountBalance = models.DecimalField(decimal_places=2)

class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    customerName = models.CharField(max_length=50, default='')
    pickUpTime = models.DateTimeField('pickUpTime')
    items = models.CharField(default='[]')
    totalCost = models.DecimalField(decimal_places=2)
    isPrepared = models.BooleanField()
    isFufilled = models.BooleanField()
    

class InventoryItem(models.Model):
    price = models.DecimalField(decimal_places=2)
    stock = models.IngeterField()
    name = models.CharField(max_length=50, default='')
    description = models.TextField()
    allegryInfo = models.CharField(max_length=50, default='')
    
    ITEMTYPE = (
        ('ba', 'bagel'),
        ('be', 'beverage'),
        ('sc', 'Schmear'),
        ('sa', 'sandwich'),
    )
    
    type = models.CharField(
        max_length=2,
        choices=ITEMTYPE,
        blank=True,
        default='ba',
        help_text='Item type',
    )    
