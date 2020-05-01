from django.contrib import admin
from .models import Product, ProductImage


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


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)

