from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import generic
from .forms import SignUpForm
from .models import Order, InventoryItem

# Create your views here.


def index(request):
    return render(request, 'bagels/index.html')


def signUp(request):
    if request.user.is_authenticated:
        return redirect('home')

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


def cancelOrder(request, order_id):
    order = Order.objects.get(pk=order_id)

    request.user.profile.account_balance += order.total_cost
    request.user.save()

    order.is_fufilled = True
    order.save()

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

    context = {'ba': ba_list, 'be' : be_list, 'sc' : sc_list, 'sa' : sa_list,
        'user': request.user}
    return render(request, 'bagels/index.html', context)

# def placeOrder(request):
#     ordered = []
#     try:
#         cust = Profile.objects.get(pk=request.POST['customer'])
#         order_string = request.POST.get("items")
#         order_items = order_string.split(', ')
#         for item in order_items
#
#     except Exception as e:
#         return render(request, 'bagels/index.html', {
#             'item_list': InventoryItem.objects.all(),
#             'error_message': "Please select an item in order to place an order"
#         })
#     else:
#
#
#         try:
#             for


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
