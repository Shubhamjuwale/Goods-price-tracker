from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import SignUpForm
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
         
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1']) 
            user.save()
            login(request, user) 
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'tracker/signup.html', {"form": form})


def login_view(request):  
    return render(request, 'tracker/login.html')

def dashboard(request):
    guest = request.GET.get("guest", False)
    return render(request, 'tracker/dashboard.html', {"guest": guest})

def search(request):
    return render(request, 'tracker/search.html')

def review(request):
    return render(request, 'tracker/review.html')

def edit_watchlist(request):
    return render(request, "edit_watchlist.html")
