from django.contrib import admin
from .models import Product, Category, Order, Shipping
#Register 
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Shipping)
