from django.contrib import admin
from .models import Customer, Product, Cart, OrderPlaced
from django.utils.html import format_html
from django.urls import reverse
# Register your models here.


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']
    
    
    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description',
                    'brand', 'categury', 'Product_image']
    
    
@admin.register(Cart)
class CartMOdelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    
    
@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'Customer_info', 'product', 'Product_info',
                    'quantity', 'ordered_date', 'status']
    
    
    # create function to link.
    def Customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href = "{}"> "{}"</a> ', link, obj.customer.name)
    
    
    
    # create function to link.
    def Product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href = "{}"> "{}"</a> ', link, obj.product.title)
    
