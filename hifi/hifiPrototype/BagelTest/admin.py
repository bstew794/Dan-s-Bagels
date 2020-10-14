from django.contrib import admin

from .models import Order, Menu_Item

# Register your models here.
admin.site.register(Order)
admin.site.register(Menu_Item)
