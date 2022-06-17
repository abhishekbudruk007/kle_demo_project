from django.shortcuts import render
from products.models import Product
from users.models import CustomUsers
from django.views.generic.list import ListView
# Create your views here.


# def home(request):
#     fruits_objects = Product.objects.all() #select * from Product
#     return render(request, 'dashboard/index.html', context={"products":fruits_objects})

class HomePageView(ListView):
    model = Product
    template_name = 'dashboard/index.html'
    context_object_name = 'products'

def shop(request):
    context_objects = [{"name":"Abhishek", "age":"29"}, {"name":"Rutuja", "age":"23"}, {"name":"Lobo", "age":"24"}]
    return render(request, 'dashboard/shop.html', context={"objects":context_objects})

def about(request):
    print("This is Home Page")
    return render(request, 'dashboard/about.html')