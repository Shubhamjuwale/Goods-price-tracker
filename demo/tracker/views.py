from django.shortcuts import render

def signup(request):
    return render(request, 'tracker/signup.html')

def login(request):
    return render(request, 'tracker/login.html')

def dashboard(request):
    return render(request, 'tracker/dashboard.html')

def search(request):
    return render(request, 'tracker/search.html')

def review(request):
    return render(request, 'tracker/review.html')

def edit_watchlist(request):
    return render(request, 'tracker/edit_watchlist.html')
