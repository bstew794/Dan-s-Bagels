from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from forms import SignUpForm

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
            
            return redirect('BLANK')
        
    else:
        form = SignUpForm()
        
    return render(request, 'signup.html', {'form': form})
