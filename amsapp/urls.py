from django.urls import path
from . import views

urlpatterns = [
    path('',views.home , name="home"),
    
    
    path('register/',views.registerPage, name="register"),
    path('login/', views.loginPage , name="login"),
    path('logout/',views.logoutUser , name="logout"),


    path('user/', views.userPage , name="user-page"),
    path('account/', views.accountSettings , name="accounts"),
    
    path('product/',views.products , name="products"),
    path('customer/<str:id>',views.customer , name="customer" ),
    path('order/<str:id>',views.create_order , name="order"),
    path('update/<str:id>',views.update_order , name="updateorder"),
    path('delete/<str:id>',views.delete_order , name="deleteorder"),
]
