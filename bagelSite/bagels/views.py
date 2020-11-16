from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import InventoryItem

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

def mainMenu(request):
    menu_list = InventoryItem.objects.all()

    context = {'inventory_list': menu_list,}
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
