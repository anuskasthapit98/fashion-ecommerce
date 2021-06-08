from django.contrib import admin
from .models import*
# Register your models here.


admin.site.register([Account,Customer, Category, Brands, Products, ProductImage, Coupon, Order, Size])
