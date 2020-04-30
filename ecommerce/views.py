from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'ecommerce/index.html')


def register_page(request):
    return render(request, 'ecommerce/register.html')


def login_page(request):
    return render(request, 'ecommerce/login.html')


def shopping_cart(request):
    return render(request, 'ecommerce/shopping-cart.html')


def shop(request):
    return render(request, 'ecommerce/shop.html')


def contact_page(request):
    return render(request, 'ecommerce/contact.html')