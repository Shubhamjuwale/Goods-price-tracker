from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import SignUpForm
from .models import Watchlist, Product, Review
from django.db.models import Q,Avg
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages  
from django.contrib.auth.hashers import make_password  
import json
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
            request.session["is_guest"] = False  
            return redirect("dashboard")
        else:
            password_error = "Incorrect password"

    return render(request, "tracker/login.html", {
        "username_error": username_error,
        "password_error": password_error,
    })

def dashboard(request):
    tags = ['tag1', 'tag2']  # or get from database
    products = Product.objects.all()  # or filtered queryset
    selected_tag = request.GET.get('tag', 'all')
    limit = int(request.GET.get('limit', 20))

    context = {
        'tags': tags,
        'products': products[:limit],
        'selected_tag': selected_tag,
        'limit': limit,
    }

    
    if not request.user.is_authenticated and request.GET.get("guest") == "true":
        request.session["is_guest"] = True
    elif request.user.is_authenticated:
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

def add_to_watchlist(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    # Get first watchlist of the logged-in user
    watchlist = Watchlist.objects.filter(user=request.user).first()
    if watchlist:
        watchlist.products.add(product)
    # Redirect to watchlist page
    return redirect('watchlist') 

def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    watchlists = Watchlist.objects.filter(user=request.user)

    # Get price history
    prices = product.prices.order_by('price_date')
    labels = [p.price_date.strftime('%b') for p in prices]
    data = [p.price for p in prices]

    # Calculate Peak Month, Low Month, Best Time to Buy
    # Create a dict with month abbreviation as key and average price as value
    month_price_dict = {}
    for p in prices:
        month_abbr = p.price_date.strftime('%b')
        if month_abbr not in month_price_dict:
            month_price_dict[month_abbr] = []
        month_price_dict[month_abbr].append(p.price)

    # Average price per month
    avg_month_price = {month: sum(prices)/len(prices) for month, prices in month_price_dict.items()}

    if avg_month_price:
        peak_month = max(avg_month_price, key=avg_month_price.get)
        low_month = min(avg_month_price, key=avg_month_price.get)
        best_time_to_buy = low_month
    else:
        peak_month = low_month = best_time_to_buy = None

    return render(request, "tracker/product_detail.html", {
        "product": product,
        "watchlists": watchlists,
        "labels_json": json.dumps(labels),
        "data_json": json.dumps(data),
        "peak_month": peak_month,
        "low_month": low_month,
        "best_time_to_buy": best_time_to_buy,
    })

def search_products(request):
    query = request.GET.get("q", "").strip()
    results = []

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__icontains=query) | Q(tag__icontains=query)
        )[:10] 
        results = [
            {"id": p.pk, "name": p.name}
            for p in products
        ]

    return JsonResponse({"results": results})

def review(request):
   
    if request.session.get("is_guest", False):
        return render(request, "tracker/guest_restricted.html", {"feature": "Review"})

   
    if not request.user.is_authenticated:
        return render(request, "tracker/guest_restricted.html", {"feature": "Review"})

   
    if request.method == "POST":
        comment = request.POST.get("comment")
        if comment:
            Review.objects.create(
                user=request.user,
                comment=comment,
            )

    reviews = Review.objects.filter(user=request.user).order_by("-date")
    return render(request, "tracker/review.html", {"reviews": reviews})

def watchlist(request):
    if request.session.get("is_guest", False):
        return render(request, "tracker/guest_restricted.html", {"feature": "Watchlist"})
    if not request.user.is_authenticated:
        return render(request, "tracker/guest_restricted.html", {"feature": "Watchlist"})
    
    watchlists = Watchlist.objects.filter(user=request.user)
    return render(request, "tracker/watchlist.html", {"watchlists": watchlists})
    return render(request, "watchlist.html", {"watchlists": watchlists})

@login_required
def create_watchlist(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if name:
            if len(name) > 20:
                name = name[:20]
            Watchlist.objects.create(user=request.user, name=name)
        return redirect("watchlist")
    return render(request, "tracker/create_watchlist.html")

@login_required
def remove_watchlist(request, watchlist_id):
    wl = get_object_or_404(Watchlist, watchlist_id=watchlist_id, user=request.user)
    wl.delete()
    return redirect("watchlist")

@login_required
def remove_item(request, watchlist_id, product_id):
    wl = get_object_or_404(Watchlist, watchlist_id=watchlist_id, user=request.user)
    product = get_object_or_404(Product, product_id=product_id)
    wl.products.remove(product)
    return redirect("watchlist")

@login_required
def add_item(request, watchlist_id, product_id):
    wl = get_object_or_404(Watchlist, id=watchlist_id, user=request.user)
    product = get_object_or_404(Product, id=product_id)
    wl.products.add(product)
    return redirect("dashboard")

# AJAX endpoints
@login_required
def ajax_show_more_watchlist_items(request, watchlist_id):
    wl = get_object_or_404(Watchlist, id=watchlist_id, user=request.user)
    offset = int(request.GET.get("offset", 5))
    products = wl.products.all()[offset:offset+5]
    items = [{"id": p.id, "name": p.name, "price": p.price} for p in products]
    return JsonResponse({"items": items})

@login_required
def ajax_add_product_to_watchlist(request):
    if request.method == "POST":
        wl_id = request.POST.get("watchlist_id")
        product_id = request.POST.get("product_id")
        wl = get_object_or_404(Watchlist, id=wl_id, user=request.user)
        product = get_object_or_404(Product, id=product_id)
        wl.products.add(product)
        return JsonResponse({"success": True, "message": f"{product.name} added to {wl.name}"})

def ajax_add_to_watchlist(request):
    if request.method == "POST":
        wl_id = request.POST.get("watchlist_id")
        product_id = request.POST.get("product_id")

        try:
            watchlist = Watchlist.objects.get(watchlist_id=wl_id, user=request.user)
            product = Product.objects.get(product_id=product_id)
            watchlist.products.add(product)
            return JsonResponse({"success": True, "message": f"{product.name} added to {watchlist.name}!"})
        except Watchlist.DoesNotExist:
            return JsonResponse({"success": False, "message": "Watchlist not found!"})
        except Product.DoesNotExist:
            return JsonResponse({"success": False, "message": "Product not found!"})
    
    return JsonResponse({"success": False, "message": "Invalid request."})
def forgot_password(request):
    errors = {}
    success = ""

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        new_username = request.POST.get("username", "").strip()
        new_password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            errors["email"] = "No user found with this email."

        
        if not (8 <= len(new_username) <= 15):
            errors["username"] = "Username must be 8-15 characters long."
        elif User.objects.filter(username=new_username).exclude(email=email).exists():
            errors["username"] = "Username is already in use."

        
        if not (8 <= len(new_password) <= 15):
            errors["password"] = "Password must be 8-15 characters long."
        if new_password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."

        
        if not errors:
            user.username = new_username
            user.password = make_password(new_password)
            user.save()
            success = "Username and password updated successfully."
            return redirect("login")

    return render(request, "tracker/forgot_password.html", {
        "errors": errors,
        "success": success,
        "email_value": request.POST.get("email", ""),
        "username_value": request.POST.get("username", "")
    })
