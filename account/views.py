from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from itasset.models import Company

# Create your views here.

# Function to login
def login_view(request):
    if request.method == 'GET':        
        nexturl = request.GET.get('next')
        print(request)
        return render(request, 'login.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)       
        # Redirect to a success page.
        if request.GET.get('next'):
            return redirect(request.GET.get('next'))
        else:
            return redirect('/')
    else:
        # Return an 'invalid login' error message.    
        # return redirect(request.get_full_path())
        return render(request,'login.html',{'msg':'Bad user name or password!'})

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect(reverse('login'))

# Function for password chagne done
def passwordChangeDone_view(request):
    return redirect('/')
