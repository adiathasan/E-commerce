from django.contrib import admin
from .models import Product, ProductImage, Customer, ShippingAddress, OrderItem, Order


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'time_stamp'
    list_display = ['title', 'price', 'discount_price', 'active', 'Updated']
    list_editable = ['price', 'active', 'discount_price']
    list_filter = ['price', 'active']
    search_fields = ['title', 'price']
    readonly_fields = ['time_stamp', 'Updated']

    class meta:
        model = Product


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['complete', 'customer']
    readonly_fields = ['date_ordered']
    date_hierarchy = 'date_ordered'
    list_display = ['customer', 'date_ordered', 'complete']

    class Meta:
        model = Order


class OrderItemAdmin(admin.ModelAdmin):
    list_filter = ['order', 'date_added']
    readonly_fields = ['date_added']
    date_hierarchy = 'date_added'
    list_display = ['product', 'order', 'date_added', 'quantity']

    class Meta:
        model = Order


admin.site.register(Customer)

admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)

admin.site.register(Order, OrderAdmin)

admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(ShippingAddress)
