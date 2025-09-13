from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import SignUpForm
from .models import Watchlist, Product
from django.db.models import Q
from django.http import JsonResponse
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  
            user.save()

           
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'tracker/signup.html', {"form": form})


    return render(request, 'tracker/signup.html', {"form": form})


def login_view(request):
    username_error = ""
    password_error = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            username_error = "Incorrect username"
            return render(request, "tracker/login.html", {
                "username_error": username_error,
                "password_error": password_error,
            })

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session["is_guest"] = False  # clear guest mode
            return redirect("dashboard")
        else:
            password_error = "Incorrect password"

    return render(request, "tracker/login.html", {
        "username_error": username_error,
        "password_error": password_error,
    })

def dashboard(request):
    if request.GET.get("guest") == "true":
        request.session["is_guest"] = True
    else:
        request.session["is_guest"] = False
    tag = request.GET.get("tag", "all")
    products = Product.objects.all()

    if tag != "all":
        products = products.filter(tag__icontains=tag)

    limit = int(request.GET.get("limit", 20))
    products = products[:limit]

    tags = list(Product.objects.values_list("tag", flat=True).distinct())

    return render(request, "tracker/dashboard.html", {
        "products": products,
        "tags": tags,
        "selected_tag": tag,
        "limit": limit,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "tracker/product_detail.html", {"product": product})

def search_products(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__icontains=query) | Q(tag__icontains=query)
        )[:10]  # limit results to 10 for now
        results = [
            {"id": p.pk, "name": p.name}
            for p in products
        ]

    return JsonResponse({"results": results})

def review(request):
    # If guest mode, show restriction
    if request.session.get("is_guest", False):
        return render(request, "tracker/guest_restricted.html", {"feature": "Review"})

    # If not logged in, also restrict
    if not request.user.is_authenticated:
        return render(request, "tracker/guest_restricted.html", {"feature": "Review"})

    # Otherwise show normal review page
    return render(request, "tracker/review.html")
def edit_watchlist(request):
    return render(request, "tracker/edit_watchlist.html")
def watchlist(request):
    if request.session.get("is_guest", False):
        return render(request, "tracker/guest_restricted.html", {"feature": "Watchlist"})
    if not request.user.is_authenticated:
        return render(request, "tracker/guest_restricted.html", {"feature": "Watchlist"})
    
    watchlists = Watchlist.objects.filter(user=request.user)
    return render(request, "tracker/watchlist.html", {"watchlists": watchlists})
    return render(request, "watchlist.html", {"watchlists": watchlists})

def forgot_password(request):
    return render(request, "tracker/forgot_password.html")
