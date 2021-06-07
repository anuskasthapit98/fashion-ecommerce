from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User, Group
import datetime
from django.utils import timezone

# Create your models here.


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, hard=False):
        if not hard:
            self.deleted_at = timezone.now()
            return super().save()
        else:
            return super().delete()


class Category(TimeStamp):
    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to="category")
    parent = models.ForeignKey('self', related_name="sub_Category", on_delete=models.CASCADE, null=True , blank= True, ) 
    slug = models.SlugField(unique= True, primary_key= True)
    description = RichTextField()
    
    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')

    def __str__(self):
                                   
        full_path = [self.name]            
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])

    
class Brands(TimeStamp):
    name = models.CharField(max_length=250)
    logo = models.ImageField(upload_to="brands")

    class Meta:
        verbose_name = ('Brand')
        verbose_name_plural = ('Brands')

    def __str__(self):
        return self.name


class ProductImage(TimeStamp):
    image = models.ImageField(upload_to="products")


class Products(TimeStamp):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    brands = models.ForeignKey(Brands, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ManyToManyField(ProductImage)
    description = RichTextField()
    price = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, primary_key=True)
    vat_incl = models.BooleanField(default=False)
    vat_percent = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    vat_amt = models.DecimalField(null=True, max_digits=12, decimal_places=2)
    discount_percent=models.DecimalField(null=True, max_digits=12, decimal_places=2)
    discount_amt =  models.DecimalField(null=True, max_digits=12, decimal_places=2)
    view_count = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = ('Product')
        verbose_name_plural = ('Products')

    def __str__(self):
        return self.name


class Account(User):
    mobile = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    image = models.ImageField(upload_to='user')

    def __str__(self):
        return self.username

class Coupon(TimeStamp):
    valid_date = models.DateTimeField(null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    discount_percent=models.DecimalField(null=True, max_digits=12, decimal_places=2)
    discount_amt =  models.DecimalField(null=True, max_digits=12, decimal_places=2)
    discount_type = models.CharField(null=True, max_length=40)


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)
      
class Order(TimeStamp):
    product = models.ManyToManyField(Products)
    shipping_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)

    def __str__(self):
        return "Order: " + str(self.id)
