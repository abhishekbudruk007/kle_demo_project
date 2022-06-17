
from django.contrib import admin
from django.urls import path, include
from . import  views
app_name = "products"
urlpatterns = [
    # path('login', views.login, name="login" ),
    path('product/<int:pk>', views.DetailView, name="product_detail_view" ),
    # path('product/<int:pk>', views.DetailViewCBV.as_view(), name="product_detail_view" ),
    path('wishlist', views.WishListView.as_view(), name="wishlist" ),
    path('wishlist/<int:pk>', views.AddToWishList, name="add_to_wishlist" ),
    path('wishlist/<int:pk>/delete', views.delete_wishlist_item, name="delete_from_wishlist" ),
    path('cart_details', views.cart_details, name="cart_details" ),

    path('cart_details/<int:pk>/add', views.add_to_cart, name="add_to_cart" ),
    path('cart_details/<int:pk>/reduce', views.reduce_from_cart, name="reduce_from_cart" ),
    path('cart_details/<int:pk>/delete', views.remove_from_cart, name="remove_from_cart" ),
    path('checkout', views.checkout, name="checkout" ),
    path('payment/<payment_option>', views.payment, name='payment'),
    path("razorpay/callback/<int:pk>", views.callback, name="callback"),
]
