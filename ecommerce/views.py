from django.shortcuts import render
from .models import Product


# Create your views here.


def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'ecommerce/index.html', context)


def register_page(request):
    return render(request, 'ecommerce/register.html')


def login_page(request):
    return render(request, 'ecommerce/login.html')


def shopping_cart(request):
    return render(request, 'ecommerce/shopping-cart.html')


def shop(request):
    all_products = Product.objects.all()
    context = {'products': all_products}
    return render(request, 'ecommerce/shop.html', context)


def contact_page(request):
    return render(request, 'ecommerce/contact.html')


def product(request, pk):
    single_product = Product.objects.get(id=pk)
    all_product = Product.objects.all()
    context = {'single_product': single_product, 'all_product': all_product}
    return render(request, 'ecommerce/product.html', context)


def checkout(request):
    return render(request, 'ecommerce/check-out.html')