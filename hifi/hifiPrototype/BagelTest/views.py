from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Order

# Create your views here.
def customer(request):
    return HttpResponse("Customer Page")
    # return render(request, 'BagelTest/index.html', context)

def employee(request):
    order_list = Order.objects.order_by('-pickup_time')
    context = {'order_list': order_list,}
    return render(request, 'BagelTest/employee.html', context)
