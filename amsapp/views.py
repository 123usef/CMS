from dataclasses import field
from multiprocessing import context
from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import Group


from .models import *  
from .form import *  
from .filters import OrderFilter
from .decrators import unauthenticated_user,allowed_users , admin_only
# Create your views here.


@unauthenticated_user
def registerPage(request): 
    form = CreateUserForm()
    if request.method =="POST":
        form = CreateUserForm(request.POST)
        print(form.data)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            messages.success(request,"Account was created for " +username)

            return redirect("login")
    context={"form":form,}
    return render(request,"accounts/register.html",context)


@unauthenticated_user
def loginPage(request):   
        if request.method=="POST":
            username= request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                    login(request,user)
                    return redirect('/')
        else:
                messages.info(request,"username or password is in correct")    
        context={}
        return render(request,"accounts/login.html",context)

def logoutUser(request):

    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status = "Delivered").count()
    pending = orders.filter(status = "Pending").count()
    context = {
        "orders":orders,
        "customers" : customers,
        "total_customers":total_customers,
        "total_orders":total_orders,
        "delivered":delivered,
        "pending":pending,
    }
    return render(request , 'accounts/dashboard.html',context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status = "Delivered").count()
    pending = orders.filter(status = "Pending").count()
    print("orders:",orders)
    context={
        "orders":orders,
        "total_orders":total_orders,
        "delivered":delivered,
        "pending":pending

    }
    return render(request,'accounts/user.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST,request.FILES , instance=customer )
        if form.is_valid():
            form.save()

    context={
        "form":form,
    }
    return render(request,'accounts/account_settings.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def products(request):
    products = Product.objects.all()
    context={
        "products" : products,
    }
    return render(request , 'accounts/products.html' , context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def customer(request , id):
    cus = Customer.objects.get(id=id)
    orders = cus.order_set.all()
    total_orders = orders.count()
   
    myfilter=OrderFilter(request.GET ,queryset=orders)
    orders = myfilter.qs

    context={
        "customer":cus,
        "orders":orders,
        "total_orders":total_orders,
        "myfilter":myfilter
    }
    return render(request , 'accounts/customers.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def create_order(request,id):  
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'))  
    customer = Customer.objects.get(id=id)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer':customer})   
    if request.method== "POST":
        formset=OrderFormSet(request.POST ,instance=customer)
        # form = OrderForm(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={
        "formset":formset,
        "customer":customer,
    }    
    return render(request,'accounts/order_form.html',context)    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def update_order(request,id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST ,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={
        "form":form,
    }
    return render(request,'accounts/order_form.html',context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])

def delete_order(request,id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context={
        "item":order,
            }    
    return render(request,'accounts/delete.html',context)    