from django.contrib import admin
from .models import*
# Register your models here.


admin.site.register([Account, Customer, CategoryType, Category, Brands, Products, Tag, ProductImage, Coupon, Order, Size, Color,
                     BillingAddress, Cart, Wishlist, CartProduct, Testimonials, Blog, service, Contact, Ads, Subscription, Message, Abouts, Comment])
