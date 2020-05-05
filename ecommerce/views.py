from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout


def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_total_item
        cartPrice = order.get_total_price
    else:
        order = {'get_total_price': 0, 'get_total_item': 0, 'shipping': False}
        cartItems = order['get_total_item']
        cartPrice = order['get_total_price']
    products = Product.objects.all()
    women_products = Product.objects.filter(category='women')
    context = {'products': products, 'w_products': women_products, 'cartItems': cartItems, 'cartPrice': cartPrice}
    return render(request, 'ecommerce/index.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created Successfully by user {username}')
                return redirect('login')
        else:
            form = RegistrationForm()
        context = {'form': form}

        return render(request, 'ecommerce/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, ' invalid username or password')
        return render(request, 'ecommerce/login.html')


def logout_page(request):
    logout(request)
    return redirect('/')


def shopping_cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartPrice = order.get_total_price
        cartItems = order.get_total_item
    else:
        items = []
        order = {'get_total_price': 0, 'get_total_item': 0, 'shipping': False}
        cartItems = order['get_total_item']
        cartPrice = order['get_total_price']
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'cartPrice': cartPrice}
    return render(request, 'ecommerce/shopping-cart.html', context)


def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_total_item
        cartPrice = order.get_total_price
    else:
        order = {'get_total_price': 0, 'get_total_item': 0, 'shipping': False}
        cartItems = order['get_total_item']
        cartPrice = order['get_total_price']
    all_products = Product.objects.all()
    context = {'products': all_products, 'cartItems': cartItems, 'cartPrice': cartPrice}
    return render(request, 'ecommerce/shop.html', context)


def contact_page(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_total_item
        cartPrice = order.get_total_price
    else:
        order = {'get_total_price': 0, 'get_total_item': 0, 'shipping': False}
        cartItems = order['get_total_item']
        cartPrice = order['get_total_price']
    context = {'cartItems': cartItems, 'cartPrice': cartPrice}
    return render(request, 'ecommerce/contact.html', context)


def product(request, pk):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_total_item
        cartPrice = order.get_total_price
    else:
        order = {'get_total_price': 0, 'get_total_item': 0, 'shipping': False}
        cartItems = order['get_total_item']
        cartPrice = order['get_total_price']
    single_product = Product.objects.get(id=pk)
    all_product = Product.objects.all()
    context = {'single_product': single_product, 'all_product': all_product, 'cartItems': cartItems,
               'cartPrice': cartPrice}
    return render(request, 'ecommerce/product.html', context)


def checkout(request):
    global price_dollar
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_total_item
        cartPrice = order.get_total_price
        price_dollar = float(cartPrice) / 84.95
    else:
        items = []
        order = {'get_total_price': 0, 'get_total_item': 0, 'shipping': False}
        cartItems = order['get_total_item']
        cartPrice = order['get_total_price']
    context = {'items': items, 'order': order, 'cartItems': cartItems,
               'cartPrice': cartPrice, 'price_dollar': price_dollar}
    return render(request, 'ecommerce/check-out.html', context)


def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product_1 = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product_1)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_Id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_Id

        if total == float(order.get_total_item):
            order.complete = True
        order.save()
        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                phone=data['shipping']['phone'],
                address=data['shipping']['address'],
                Zip_code=data['shipping']['zip'],
                city=data['shipping']['city'],
            )
            return redirect('home')
    return JsonResponse('payment completed.', safe=False)


def search(request):
    try:
        query = request.GET.get('q')
    except:
        q = None

    if query:
        products = Product.objects.filter(Q(title__icontains=query) | Q(category__icontains=query))

        template = 'ecommerce/result.html'
        context = {'query': query, 'products': products}
    else:
        template = 'ecommerce/shop.html'
        products = Product.objects.all()
        context = {'products': products}
    return render(request, template, context)


def men_page(request):
    products = Product.objects.filter(category='men')
    template = 'ecommerce/men.html'
    context = {'products': products}
    return render(request, template, context)


def women_page(request):
    products = Product.objects.filter(category='women')
    context = {'products': products}
    return render(request, 'ecommerce/women.html', context)


def kids_page(request):
    products = Product.objects.filter(category='kids')
    template = 'ecommerce/kids.html'
    context = {'products': products}
    return render(request, template, context)


def accessories_page(request):
    products = Product.objects.filter(category='accessories')
    template = 'ecommerce/accessories.html'
    context = {'products': products}
    return render(request, template, context)