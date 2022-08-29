from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return HttpResponse("hello there from home ")



def products(request):
    return HttpResponse("hello there from products ")

def customer(request):
    return HttpResponse("hello there from customer ")