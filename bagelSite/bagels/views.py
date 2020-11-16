from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import generic
from .forms import SignUpForm
from .models import Order

# Create your views here.


def index(request):
    return render(request, 'bagels/index.html')


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


class CurrentOrderListView(generic.ListView):
    model = Order
    context_object_name = 'current_orders_list'
    template_name = 'bagels/current_orders.html'

    def get_queryset(self):
        return Order.objects.filter(is_fufilled=False)
