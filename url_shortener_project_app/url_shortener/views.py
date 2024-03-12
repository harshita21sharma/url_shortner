import shortuuid
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import URL, Click
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max



def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            message = "User doesn't exist. Please sign up."
            return render(request, "login.html", {'message': message})
        
        if check_password(password, user.password):
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, "login.html", {'message': ""})
    else:
        return render(request, "login.html", {'message': ""})

def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'user_register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'user_register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email address already exists.")
            return render(request, 'user_register.html')

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, "Thank you for signing up. Please login to continue.")
        return redirect('dashboard')
    else:
        return render(request, 'user_register.html')


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")

@login_required(login_url='/login/')
def shorten_url(request):
    if request.method == "POST":
        long_url = request.POST.get("long_url")
        if not long_url.startswith(("http://", "https://")):
            return render(request, "create_url.html", {"error_message": "URL must start with 'http://' or 'https://'"})

        short_alias = shortuuid.uuid()[:10]
        user = request.user
        url = URL.objects.create(original_url=long_url, short_alias=short_alias, created_by=user)        
        return render(request, "shorten_success.html", {"short_alias": url.short_alias})
    return render(request, "create_url.html")

def redirect_to_long_url(request, short_alias):    
    url = get_object_or_404(URL, short_alias=short_alias)
    return redirect(url.original_url)

def dashboard(request):
    combined_data = []
    urls = URL.objects.annotate(
        num_clicks=Count('click'),
        last_clicked=Max('click__clicked_at')
    )

    for url in urls:
        clicks = Click.objects.filter(url=url)
        ip_addresses = [click.ip_address for click in clicks]
        analytics_data = {
            'short_alias': url.short_alias,
            'original_url': url.original_url,
            'clicks': url.num_clicks,
            'last_clicked': url.last_clicked,
            'ip_addresses': ip_addresses
        }
        combined_data.append(analytics_data)

    return render(request, 'dashboard.html', {'combined_data': combined_data})