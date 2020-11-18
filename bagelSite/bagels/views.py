from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import generic
from .forms import SignUpForm
from .models import Order, InventoryItem, Profile
from django.utils import timezone
from decimal import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

# Create your views here.



def signUp(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('home')

    else:
        form = SignUpForm()

    return render(request, 'bagels/signup.html', {'form': form})


def fulfillOrder(request, order_id):
    order = Order.objects.get(pk=order_id)

    order.is_fufilled = True
    order.save()

    return redirect('current_orders')


def prepareOrder(request, order_id):
    order = Order.objects.get(pk=order_id)

    order.is_prepared = True
    order.save()

    return redirect('current_orders')


def home(request):
    ba_list = InventoryItem.objects.filter(type='ba')
    be_list = InventoryItem.objects.filter(type='be')
    sc_list = InventoryItem.objects.filter(type='sc')
    sa_list = InventoryItem.objects.filter(type='sa')

    context = {'ba': ba_list, 'be' : be_list, 'sc' : sc_list, 'sa' : sa_list,
        'user': request.user}
    return render(request, 'bagels/index.html', context)

def placeOrder(request):
    string_list = ', '
    try:
        current_user = Profile.objects.filter(user=request.user).first()
        chosen_items = request.POST.getlist('item')
        object_list = []
        for item in chosen_items:
            i = InventoryItem.objects.get(pk=item)
            object_list.append(i)

    except (KeyError, Menu_Item.DoesNotExist):
        ba_list = InventoryItem.objects.filter(type='ba')
        be_list = InventoryItem.objects.filter(type='be')
        sc_list = InventoryItem.objects.filter(type='sc')
        sa_list = InventoryItem.objects.filter(type='sa')

        context = {'ba': ba_list, 'be' : be_list, 'sc' : sc_list, 'sa' : sa_list,
            'user': request.user}
        return render(request, 'home', context)

    else:
        cost = 0.00
        for o in object_list:
            cost += float(o.price)
        string_list = string_list.join([elem.name for elem in object_list])

        new_order = Order(customer=current_user,
        customer_name=request.user.first_name, pickup_time=timezone.now(),
        items=string_list, total_cost=cost, is_prepared=False, is_fufilled=False)
        new_order.save()
        return HttpResponseRedirect(reverse('profile'))






class CurrentOrderListView(generic.ListView):
    model = Order
    context_object_name = 'current_orders_list'
    template_name = 'bagels/current_orders.html'

    def get_queryset(self):
        return Order.objects.filter(is_fufilled=False)


def profile(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'bagels/profile.html', {"user": user})
    else:
        return redirect("login")
