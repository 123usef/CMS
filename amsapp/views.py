from dataclasses import field
from multiprocessing import context
from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from .models import *  
from .form import *  
from .filters import OrderFilter
# Create your views here.

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


def products(request):
    products = Product.objects.all()
    context={
        "products" : products,
    }
    return render(request , 'accounts/products.html' , context)

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

def delete_order(request,id):
    order = Order.objects.get(id=id)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context={
        "item":order,
            }    
    return render(request,'accounts/delete.html',context)    