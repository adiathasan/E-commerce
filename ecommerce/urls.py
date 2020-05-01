from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('shopping-cart/', shopping_cart, name='shopping-cart'),
    path('shop/', shop, name='shop'),
    path('contact/', contact_page, name='contact'),
    path('product/<str:pk>/', product, name='product'),
    path('checkout/', checkout, name='checkout'),
]