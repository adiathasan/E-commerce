from django.db import models


# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=31.50)
    discount_price = models.DecimalField(decimal_places=2, max_digits=100, default=31.50)
    time_stamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    Updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
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


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='side_image')
    image = models.ImageField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.product.title
