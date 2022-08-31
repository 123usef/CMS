from django.urls import path
from . import views

urlpatterns = [
    path('',views.home , name="home"),
    path('product/',views.products , name="products"),
    path('customer/<str:id>',views.customer , name="customer" ),
    path('order/',views.create_order , name="order")
]
