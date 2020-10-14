from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Order, Menu_Item

# Create your views here.
def customer(request):

    item_list = Menu_Item.objects.all()
    context = {'item_list': item_list,}
    return render(request, 'BagelTest/customer.html', context)

def employee(request):
    order_list = Order.objects.order_by('-pickup_time')
    context = {'order_list': order_list,}
    return render(request, 'BagelTest/employee.html', context)
