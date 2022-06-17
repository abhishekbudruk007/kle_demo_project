from django.shortcuts import render , redirect
from .models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Wishlist, OrderItem
from django.views.generic.list import ListView

# Create your views here.
def DetailView(request,pk):
    product_fetched = Product.objects.filter(id=pk)[0]
    context={
        "product": product_fetched
    }
    return render(request,'products/product_detail_view.html',context)


# class DetailViewCBV(LoginRequiredMixin,DetailView):
#    model = Product
#    template_name = "products/product_detail_view.html"

@login_required
def AddToWishList(request,pk):
   product_object = Product.objects.filter(id=pk)[0]

   wishlist_object ,created = Wishlist.objects.get_or_create(
       wishlist_user = request.user,
       wishlist_product=product_object
   )

   messages.success(request, 'Product Added to Wishlist')
   return redirect('dashboard:home')



class WishListView(LoginRequiredMixin, ListView):
   template_name = 'products/wishlist.html'
   context_object_name = 'wishlists'
   def get_queryset(self):
       query_set = Wishlist.objects.filter(wishlist_user=self.request.user)
       print("query_set",query_set)
       return query_set


def delete_wishlist_item(request, pk):
    print("I am inside Delete Functionality")
    object = Wishlist.objects.filter(id=pk, wishlist_user=request.user)
    object.delete()
    messages.error(request, "Item from Wishlist is deleted successfully")
    return redirect('products:wishlist')


def cart_details(request):
    # import pdb;pdb.set_trace()
    # cart_objects = OrderItem.objects.filter(orderitem_user= request.user)
    order_objects = Order.objects.filter(user = request.user, ordered =False )
    print("order_objects",  order_objects)
    context = {}
    if order_objects:
        order_objects = order_objects[0]
        context= {
            'order_objects': order_objects
        }

    return render(request, 'products/cart.html', context)


from django.utils import timezone
from .models import Order, OrderItem
from django.shortcuts import redirect , get_object_or_404

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # product = Product.objects.filter(id=pk)[0]
    order_product, created = OrderItem.objects.get_or_create(
      orderitem_product=product,
      orderitem_user=request.user,
      orderitem_ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
      order = order_qs[0]

      if order.products.filter(orderitem_product__pk=product.pk).exists():
          order_product.orderitem_quantity += 1
          order_product.save()
          messages.info(request, "Added quantity Item")
          return redirect('products:cart_details')
      else:
          order.products.add(order_product)
          messages.info(request, "Item added to your cart")
          return redirect('products:cart_details')
    else:
      ordered_date = timezone.now()
      order = Order.objects.create(user=request.user, ordered_date=ordered_date)
      order.products.add(order_product)
      messages.info(request, "Item added to your cart")
      return redirect('products:cart_details')


def reduce_from_cart(request, pk):
   product = get_object_or_404(Product, pk=pk)
   order_qs = Order.objects.filter(
       user=request.user,
       ordered=False
   )
   if order_qs.exists():
       order = order_qs[0]
       if order.products.filter(orderitem_product__pk=product.pk).exists():
           order_item = OrderItem.objects.filter(
               orderitem_product=product,
               orderitem_user=request.user,
               orderitem_ordered=False
           )[0]
           if order_item.orderitem_quantity > 1:
               order_item.orderitem_quantity -= 1
               order_item.save()
           else:
               order_item.delete()
           messages.info(request, "Item quantity was updated")
           return redirect("products:cart_details")
       else:
           messages.info(request, "This Item not in your cart")
           return redirect("products:cart_details")
   else:
       # add message doesnt have order
       messages.info(request, "You do not have an Order")
       return redirect("products:cart_details")


def remove_from_cart(request, pk):
  product = get_object_or_404(Product, pk=pk)
  order_qs = Order.objects.filter(
      user=request.user,
      ordered=False
  )
  if order_qs.exists():
      order = order_qs[0]
      if order.products.filter(orderitem_product__pk=product.pk).exists():
          order_item = OrderItem.objects.filter(
              orderitem_product=product,
              orderitem_user=request.user,
              orderitem_ordered=False
          )[0]
          order_item.delete()
          messages.info(request, "Item \""+order_item.orderitem_product.product_name+"\" remove from your cart")
          return redirect("products:cart_details")
      else:
          messages.info(request, "This Item not in your cart")
          return redirect("products:cart_details")
  else:
      messages.info(request, "You do not have an Order")
      return redirect("products:cart_details")

from .forms import CheckoutForm
from .models import CheckoutAddress
def checkout(request):
   if request.method == "POST":
       form = CheckoutForm(request.POST or None)
       # import pdb;pdb.set_trace()
       try:
           order = Order.objects.get(user=request.user, ordered=False)
           if form.is_valid():
               street_address = form.cleaned_data.get('street_address')
               apartment_address = form.cleaned_data.get('apartment_address')
               country = form.cleaned_data.get('country')
               zip = form.cleaned_data.get('zip')

               payment_option = form.cleaned_data.get('payment_option')

               checkout_address = CheckoutAddress(
                   user=request.user,
                   street_address=street_address,
                   apartment_address=apartment_address,
                   country=country,
                   zip=zip
               )
               checkout_address.save()
               order.checkout_address = checkout_address
               order.save()
               if payment_option == 'C':
                   order.payment = payment_option
                   order.ordered = True
                   order.save()
                   messages.add_message(request, messages.SUCCESS, "Ordered Successfully")
                   return redirect('dashboard:home')
               elif payment_option == 'S':
                   return redirect('products:payment', payment_option='stripe')
               elif payment_option == 'R':
                   return redirect('products:payment', payment_option='razorpay')
               else:
                   messages.warning(request, "Invalid Payment option")
                   return redirect('products:checkout')

       except Exception as e:
           messages.error(request, "You do not have an order")
           return redirect("products:cart_details")
   else:
       form = CheckoutForm()
       order = Order.objects.get(user=request.user, ordered=False)
       context = {
           'form': form,
           'order': order
       }
       return render(request, 'products/checkout.html', context)


from django.conf import settings
from .models import Payments
import razorpay


@login_required
def payment(request, payment_option):
    # import pdb;pdb.set_trace()
    order = Order.objects.get(user=request.user, ordered=False)
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create(
        {"amount": int(order.get_total_price()) * 100, "currency": "INR", "payment_capture": "1"}
    )
    payment_object = Payments()
    payment_object.provider_order_id = razorpay_order['id']
    payment_object.user = request.user
    payment_object.amount = order.get_total_price()
    payment_object.save()

    order.payment = payment_object
    order.save()

    return render(
        request,
        "products/payment.html",
        {
            "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback",
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order": order,
            "user": request.user
        },
    )


from django.views.decorators.csrf import csrf_exempt
from users.models import CustomUsers
import json


@csrf_exempt
def callback(request, pk):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    user = CustomUsers.objects.filter(id=pk)
    if user:
        user = user[0]
        order = Order.objects.get(user=user, ordered=False)
        if "razorpay_signature" in request.POST:
            payment_id = request.POST.get("razorpay_payment_id", "")
            provider_order_id = request.POST.get("razorpay_order_id", "")
            signature_id = request.POST.get("razorpay_signature", "")

            payment_object = Payments.objects.get(provider_order_id=provider_order_id)
            payment_object.payment_id = payment_id
            payment_object.signature_id = signature_id
            payment_object.save()

            if verify_signature(request.POST):
                order.ordered = True
                order.save()
                return render(request, "products/callback.html", context={"status": order.ordered})
            else:
                order.ordered = False
                order.save()
                return render(request, "products/callback.html", context={"status": order.ordered})
        else:
            payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
            provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
                "order_id"
            )
            payment_object = Payments.objects.get(provider_order_id=provider_order_id)
            payment_object.payment_id = payment_id
            payment_object.save()
            return render(request, "products/callback.html", context={"status": order.ordered})


