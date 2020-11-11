import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


# Profile is connected to a user and serves to add more parameters and maybe methods later on
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, default='')
    member_number = models.CharField(max_length=50, default='')
    account_balance = models.DecimalField(decimal_places=2, default='0.00')

    def __str__(self):
        return self.user.username


# the next two functions make it so an instance of Profile
# is made when an instance of User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# An Order can only have one Profile but a Profile can have many Orders
class Order(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=50, default='')
    pickUp_time = models.DateTimeField('pickUpTime')
    items = models.CharField(default='[]')
    total_cost = models.DecimalField(decimal_places=2)
    is_prepared = models.BooleanField()
    is_fufilled = models.BooleanField()

    def __str__(self):
        return f'{self.customerName} ({self.pickUpTime})'


# basically what is on our menu, and what we are selling.
class InventoryItem(models.Model):
    price = models.DecimalField(decimal_places=2)
    stock = models.IngeterField()
    name = models.CharField(max_length=50, default='')
    description = models.TextField()
    allegry_info = models.CharField(max_length=50, default='')

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

    def __str__(self):
        return self.name
