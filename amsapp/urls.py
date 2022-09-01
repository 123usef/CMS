from django.urls import path
from . import views

urlpatterns = [
    path('',views.home , name="home"),
    path('product/',views.products , name="products"),
    path('customer/<str:id>',views.customer , name="customer" ),
    path('order/',views.create_order , name="order"),
    path('update/<str:id>',views.update_order , name="updateorder"),
    path('delete/<str:id>',views.delete_order , name="deleteorder"),
]
