
from django.contrib import admin
from django.urls import path, include
from . import  views
app_name = "users"
urlpatterns = [
    path('login', views.login, name="login" ),
    path('authenticate_user', views.authenticate_user, name="authenticate_user" ),
    path('logout', views.logout, name="logout" ),
    path('register', views.register, name="register" ),
    path('change_password', views.change_password, name="change_password" ),
]
