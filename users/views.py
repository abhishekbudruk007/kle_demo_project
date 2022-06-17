from django.shortcuts import render, HttpResponse , HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# Create your views here.


def login(request):
    return render(request, 'users/login.html')


def authenticate_user(request):
    username_str = request.POST.get('username')
    password_str = request.POST.get('password')
    if username_str and password_str:
        try:
            user = authenticate(username=username_str, password=password_str)
        except:
            messages.error(request, 'Username/Password Incorrect')
            return HttpResponseRedirect('login')
        if user is not None:
            auth_login(request, user)
            request.session['username'] = username_str
            # messages.success(request,"User is Logged In")
            return HttpResponseRedirect("/")
        else:
            messages.error(request, "Username/Password is Incorrect")
            return HttpResponseRedirect('login')
    else:
        messages.error(request, "Enter Username or Password")
    return HttpResponseRedirect('login')


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return HttpResponseRedirect('login')
    return HttpResponseRedirect('login')

from .forms import RegistrationForm
def register(request):
    registration_form = RegistrationForm()
    if request.method == "POST":
        registration_form = RegistrationForm(request.POST, request.FILES)
        if registration_form.is_valid():
            registration_form.save()
            messages.success(request, "Registration is Successfull")
            return HttpResponseRedirect('login')
        else:
            return HttpResponseRedirect('register')
    else:
        return render(request,'users/register.html', context={"form":registration_form})

from .models import CustomUsers
from django.contrib.auth.hashers import make_password,check_password

def change_password(request):

    if request.method == "POST":
        # import pdb;
        # pdb.set_trace()
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        users_object = CustomUsers.objects.filter(username=request.user.username)[0] # select * from CustomUsers where username=
        if check_password(old_password, users_object.password):
            users_object.password = make_password(new_password)
            users_object.save()
        return HttpResponseRedirect('login')
        # registration_form = RegistrationForm(request.POST, request.FILES)
        # if registration_form.is_valid():
        #     registration_form.save()
        #     messages.success(request, "Registration is Successfull")
        #     return HttpResponseRedirect('login')
        # else:
        #     return HttpResponseRedirect('register')
    else:
        return render(request,'users/change_password.html')
