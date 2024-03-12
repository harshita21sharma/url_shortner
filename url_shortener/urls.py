from django.urls import path
from .views import dashboard, redirect_to_long_url, add_user, login_user, logout_user, shorten_url



urlpatterns = [
    path('', login_user, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('register/', add_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-short-url/', shorten_url, name='create_short_url'),
    path('redirect/<str:short_alias>/', redirect_to_long_url, name='redirect_to_long_url'),
]