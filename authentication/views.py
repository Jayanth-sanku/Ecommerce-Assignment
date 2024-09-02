from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache


@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')

            
            if user.is_staff:
                return redirect(reverse('admin_dashboard'))  
            else:
                return redirect('/') 

        else:
            messages.error(request, 'Invalid username or password.')
            return redirect(reverse('login'))  

    return render(request, 'login.html')


@never_cache
def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect(reverse('login'))
