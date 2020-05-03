import uuid

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True, blank=True, unique=True, default=uuid.uuid4)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orders = self.orderitem_set.all()
        for order in orders:
            if not order.product.digital:
                shipping = True
        return shipping

    @property
    def get_total_price(self):
        orders = self.orderitem_set.all()
        total = sum([item.get_total for item in orders])
        return total

    @property
    def get_total_item(self):
        orders = self.orderitem_set.all()
        total = sum([item.quantity for item in orders])
        return total


class Product(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=31.50)
    discount_price = models.DecimalField(decimal_places=2, max_digits=100, default=31.50)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    Updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    digital = models.BooleanField(default=False)
    img = models.ImageField(blank=False, null=False, verbose_name='Image Of Product')
    CATEGORY = (
        ('men', 'men'),
        ('women', 'women'),
        ('Kids', 'kids'),
        ('accessories', 'accessories'),
    )
    category = models.CharField(max_length=50, choices=CATEGORY)

    def __str__(self):
        return self.title

    def get_price(self):
        return self.price

    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='side_image')
    image = models.ImageField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    phone = models.CharField(max_length=50, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    city = models.CharField(max_length=200, blank=False, null=False)
    Zip_code = models.CharField(max_length=200, blank=False, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
