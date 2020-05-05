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
    path('update_item/', update_item, name='update_item'),
    path('process_order/', processOrder, name='process_order'),
    path('s/', search, name='search'),
    path('logout/', logout_page, name='logout'),
    path('category/men/', men_page, name='men'),
    path('category/women/', women_page, name='women'),
    path('category/kids/', kids_page, name='kids'),
    path('category/accessories/', accessories_page, name='accessories'),
]