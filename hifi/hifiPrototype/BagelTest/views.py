from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Order, Menu_Item
from django.urls import reverse
from django.utils import timezone

# Create your views here.
def customer(request):
    item_list = Menu_Item.objects.all()
    if len(item_list) == 0:
        for i in range(5):
            s = "Menu Item " + str(i)
            m = Menu_Item(item_name=s)
            m.save()
        return HttpResponseRedirect(reverse('customer'))
        
    context = {'item_list': item_list,}
    return render(request, 'BagelTest/customer.html', context)

def employee(request):
    order_list = Order.objects.order_by('-pickup_time')
    context = {'order_list': order_list,}
    return render(request, 'BagelTest/employee.html', context)

def purchase(request):
    try:
        selected_item = Menu_Item.objects.get(pk=request.POST['item'])
    except (KeyError, Menu_Item.DoesNotExist):
        return render(request, 'BagelTest/customer.html', {
            'item_list': Menu_Item.objects.all(),
            'error_message': "You didn't select an item.",
        })
    else:
        o = Order(Items=selected_item, customer_name="Sample Customer",
        pickup_time=timezone.now())
        o.save()
        return HttpResponseRedirect(reverse('customer'))
