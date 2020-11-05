from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# An Order can only have one Customer but a Customer can have many Orders
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=50, default='')
    memberNumber = models.CharField(max_length=50, default='')
    cardNumber = models.CharField(max_length=50, default='')
    accountBalance = models.DecimalField(decimal_places=2)
    
