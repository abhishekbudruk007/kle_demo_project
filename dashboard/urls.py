
from django.contrib import admin
from django.urls import path, include
from . import  views
app_name = "dashboard"
urlpatterns = [
    # path('', views.home, name="home" ),
    path('', views.HomePageView.as_view(), name="home" ),
    path('shop', views.shop, name="shop"),
    path('about', views.about ),
]
