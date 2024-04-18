from django.shortcuts import render,redirect
from home.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate ,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    pizzas = Pizza.objects.all()
    context = {'pizzas':pizzas}
    return render(request , 'home.html',context)

def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username = username)
            if not user_obj.exists():
                messages.warning(request, "User not found.")
                return redirect('/login/')
            
            user_obj = authenticate(username = username , password = password)

            if user_obj:
                login(request,user_obj)
                return redirect('/')

            messages.success(request, "Wrong Password.")
            return redirect('/login/')
        
        except Exception as e:
            messages.error(request, "Something went wrong.")
            return redirect('/register/')
        
    return render(request , 'login.html')

def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username = username)
            if user_obj.exists():
                messages.error(request, "Username already taken.")
                return redirect('/register/')
            
            user_obj = User.objects.create(username = username)
            user_obj.set_password(password)
            user_obj.save()

            messages.success(request, "Account Created.")
            return redirect('/login/')
        
        except Exception as e:
            messages.error(request, "Something went wrong.")
            return redirect('/register/')
        
    return render(request ,'register.html')

@login_required(login_url='/login/')
def add_cart(request , pizza_uid):
    user = request.user
    pizza_obj = Pizza.objects.get(uid = pizza_uid)
    cart , _ = Cart.objects.get_or_create(user = user , is_paid = False)
    cart_items = CartItems.objects.create(
                cart = cart,
                pizza = pizza_obj
    )
    return redirect('/')

@login_required(login_url='/login/')
def cart(request):
    cart = Cart.objects.get(is_paid = False , user = request.user)
    context = {'carts' : cart}
    return render(request , 'cart.html' , context)

@login_required(login_url='/login/')
def remove_cart_items(request,cart_item_uid):
    try:
        CartItems.objects.get(uid = cart_item_uid).delete()
        return redirect('/cart/')
    except Exception as e:
        print(e)

@login_required(login_url='/login/')   
def orders(request):
    orders = Cart.objects.filter(is_paid = True , user = request.user)
    context = {'orders' : orders}
    return render(request,'orders.html' , context)

