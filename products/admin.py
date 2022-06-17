from django.contrib import admin
from .models import Product
from .models import Wishlist, OrderItem, Order
# Register your models here.




from django.contrib import admin
from .models import Product
from .models import Wishlist , OrderItem, Order, CheckoutAddress, Payments
from django.contrib.admin import DateFieldListFilter


class PaymentsFilter(admin.ModelAdmin):

   list_display = ('provider_order_id', 'payment_id',
                   'signature_id', 'user', 'amount')
   search_fields = ('user', 'amount')
   list_filter = (
       ('timestamp', DateFieldListFilter),
   )

class CheckoutAddressFilter(admin.ModelAdmin):
   list_display = ('user', 'street_address',
                   'apartment_address', 'country', 'zip')
   search_fields = ('user', 'street_address',
                   'apartment_address', 'country')

class OrderFilters(admin.ModelAdmin):
   list_display = ('user',
                   'ordered', 'checkout_address', 'payment')

class ProductFilters(admin.ModelAdmin):
   list_display = ('product_name',
                   'product_price', 'product_type', 'product_quantity')



admin.site.register(Product, ProductFilters)
admin.site.register(Wishlist)
admin.site.register(OrderItem)

admin.site.register(Order, OrderFilters)
admin.site.register(CheckoutAddress, CheckoutAddressFilter)
admin.site.register(Payments, PaymentsFilter)
