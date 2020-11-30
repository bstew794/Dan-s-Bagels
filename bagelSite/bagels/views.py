from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from decimal import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
import decimal
from .forms import SignUpForm, EditProfileForm
from .models import Order, InventoryItem, Profile


# Create your views here.


def signUp(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.member_number = user.profile.phone_number + str(
                int(round(user.date_joined.timestamp() * 1000)))
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('home')

    else:
        form = SignUpForm()

    return render(request, 'bagels/signup', {'form': form})


# Cancel an order from the current orders page
def cancelOrder(request, order_id):
    order = Order.objects.get(pk=order_id)

    request.user.profile.account_balance += order.total_cost
    request.user.save()

    order.delete()

    return redirect('current_orders')


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

    context = {'ba': ba_list, 'be': be_list, 'sc': sc_list, 'sa': sa_list,
               'user': request.user, 'num': 1}
    return render(request, 'bagels/index.html', context)


def specify(request):
    num = request.POST.get('size')
    try:
        num = int(num)
    except:
        return redirect('home')

    if num >= 0:
        ba_list = InventoryItem.objects.filter(type='ba')
        be_list = InventoryItem.objects.filter(type='be')
        sc_list = InventoryItem.objects.filter(type='sc')
        sa_list = InventoryItem.objects.filter(type='sa')

        context = {'ba': ba_list, 'be': be_list, 'sc': sc_list, 'sa': sa_list,
                   'user': request.user, 'num': num}
        return render(request, 'bagels/index.html', context)



def placeOrder(request):
    string_list = ', '
    try:
        current_user = Profile.objects.filter(user=request.user).first()
        chosen_items = request.POST.getlist('item')
        chosen_date = request.POST['Enter Pickup Time']
        object_list = []

        for item in chosen_items:
            if item != 'None':
                i = InventoryItem.objects.get(pk=item)
                object_list.append(i)

    except (KeyError, InventoryItem.DoesNotExist):
        ba_list = InventoryItem.objects.filter(type='ba')
        be_list = InventoryItem.objects.filter(type='be')
        sc_list = InventoryItem.objects.filter(type='sc')
        sa_list = InventoryItem.objects.filter(type='sa')

        context = {'ba': ba_list, 'be': be_list, 'sc': sc_list, 'sa': sa_list,
                   'user': request.user, 'num': 1}
        return render(request, 'home', context)

    else:
        if chosen_date is None or chosen_date == "":
            chosen_date = timezone.now();
        if len(object_list) <= 0:
            return redirect('home')
        else:
            cost = 0.00
            for o in object_list:
                cost += float(o.price)
                o.stock -= 1
                o.save()
            string_list = string_list.join([elem.name for elem in object_list])
            final_cost = decimal.Decimal(cost)
            request.user.profile.account_balance -= final_cost
            request.user.save()


            new_order = Order(customer=current_user,
                              customer_name=request.user.first_name, pickup_time=chosen_date,
                              items=string_list, total_cost=cost, is_prepared=False, is_fufilled=False)

            new_order.save()
            return HttpResponseRedirect(reverse('profile'))


class CurrentOrderListView(generic.ListView):
    model = Order
    context_object_name = 'current_orders_list'
    template_name = 'bagels/current_orders.html'

    def get_queryset(self):
        return Order.objects.filter(is_fufilled=False)


# Returns the profile page if the user is authenticated
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        orders = Order.objects.filter(customer_name=user.first_name)
        inventory = InventoryItem.objects.filter()
        return render(request, 'bagels/profile.html', {"user": user, "orders": orders, "inventory": inventory})
    else:
        return redirect("login")


# Edits the balance of a user from the profile page
def edit(request):
    add_balance = decimal.Decimal(request.POST.get('add_balance'))
    request.user.profile.account_balance += add_balance
    request.user.save()
    return redirect("profile")


# Remove / Cancel an order from the profile page
def remove_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    # Give a refund if order is not prepared and not fulfilled
    if not order.is_prepared and not order.is_fufilled:
        request.user.profile.account_balance += order.total_cost
        request.user.save()
    # Remove order from database
    order.delete()
    return redirect('profile')


# Add stock to InventoryItems
def add_stock(request):
    inventory_items = InventoryItem.objects.all()
    for item in inventory_items:
        item.stock += int(request.POST.get(item.name))
        item.save()
    return redirect("profile")


# allow user to change credentials
def editProfile(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.member_number = user.profile.phone_number + str(
                int(round(user.date_joined.timestamp() * 1000)))
            user.save()

            return redirect('profile')

    else:
        form = EditProfileForm(instance=request.user, initial={'phone_number': request.user.profile.phone_number})

    return render(request, 'bagels/edit_profile.html', {'form': form})


# change password while logged in
def changePassword(request):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'bagels/change_password.html', {'form': form})
