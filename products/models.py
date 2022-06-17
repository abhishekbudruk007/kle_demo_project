from django.db import models
from django.conf import settings
# Create your models here.

QUANTITY_TYPE = (
    ('250GM', '250 Grams'),
    ('500GM', '500 Grams'),
    ('750GM', '750 Grams'),
    ('1000GM', '1 Kg'),
    ('1PC', '1 Pc'),
    ('12PC', '12 Pc')
)

PRODUCT_TYPE = (
    ('V', 'Vegetable'),
    ('F', 'Fruit')
)


# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField(default=0.0)
    product_discount_price = models.FloatField(blank=True, null=True)
    product_quantity_type = models.CharField(choices=QUANTITY_TYPE, max_length=6)
    product_type = models.CharField(choices=PRODUCT_TYPE, max_length=1)
    product_description = models.TextField(max_length=500, blank=True, null=True)
    product_quantity = models.IntegerField(blank=False, null=False)
    product_photo = models.ImageField(upload_to='products/', blank=False, null=False)

    def __str__(self):
        return self.product_name

class Wishlist(models.Model):
    wishlist_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    wishlist_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    wishlist_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
           return self.wishlist_product.product_name


class OrderItem(models.Model) :
   orderitem_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete=models.CASCADE)
   orderitem_product = models.ForeignKey(Product, on_delete=models.CASCADE)
   orderitem_ordered = models.BooleanField(default=False)
   orderitem_quantity = models.IntegerField(default=1)
   def __str__(self):
       return f"{self.orderitem_quantity} of {self.orderitem_product.product_name}"

   def get_total_item_price(self):
       return self.orderitem_quantity * self.orderitem_product.product_price

PAYMENT = (
  ('C', 'Cash'),
  ('S', 'Stripe'),
  ('R', 'Razorpay')
)



class Payments(models.Model):
    provider_order_id = models.CharField(max_length=40, null=True, blank=True, default="")
    payment_id = models.CharField(max_length=36, null=True, blank=True, default="")
    signature_id = models.CharField(max_length=128, null=True, blank=True, default="")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                           on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField(default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.user.username

class Order(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   products = models.ManyToManyField(OrderItem)
   start_date = models.DateTimeField(auto_now_add=True)
   ordered_date = models.DateTimeField()
   ordered = models.BooleanField(default=False)
   checkout_address = models.ForeignKey(
       'CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True)
   payment = models.ForeignKey(
       'Payments', on_delete=models.SET_NULL, blank=True, null=True)

   def __str__(self):
       return self.user.username

   def get_total_price(self):
       total = 0
       for order_item in self.products.all():
           total += order_item.get_total_item_price()
       return total

from django_countries.fields import CountryField

class CheckoutAddress(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   street_address = models.CharField(max_length=100)
   apartment_address = models.CharField(max_length=100)
   country = CountryField(multiple=False)
   zip = models.CharField(max_length=100)

   def __str__(self):
       return self.user.username


