import datetime
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User, Group
from django.db import models
from django.utils import timezone



ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti"),
    ("Esewa", "Esewa"),
)

TYPE = (
    ("Flat Discount", "Flat Discount"),
    ("Percent Discount", "Percent Discount"),
)


#Datetime Model
class DateTimeModel(models.Model):
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

#Account Model

class Account(User):
    mobile = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    image = models.ImageField(upload_to='user')
    
    class Meta:
        verbose_name = ('Account')
        verbose_name_plural = ('Accounts')
        ordering = ['-username']

    def __str__(self):
        return self.username
 
#Customer Model
   
class Customer(DateTimeModel):
    first_name =  models.CharField(max_length=50, default="New User")
    last_name =  models.CharField(max_length=50, default="New User")
    username = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = ('Customer')
        verbose_name_plural = ('Customers')
        ordering = ['-username']

    def __str__(self):
        return self.username

    
#Category Model

class Category(DateTimeModel):
    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to="category")
    parent = models.ForeignKey('self', related_name="sub_Category",
                               on_delete=models.CASCADE, null=True, blank=True, )
    slug = models.SlugField(unique=True, primary_key=True)
    description = RichTextField()

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')
        ordering = ['-slug']

    def __str__(self):

        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])

#Brand Model

class Brands(DateTimeModel):
    name = models.CharField(max_length=250)
    logo = models.ImageField(upload_to="brands")

    class Meta:
        verbose_name = ('Brand')
        verbose_name_plural = ('Brands')
        ordering = ['-name']

    def __str__(self):
        return self.name

#Size Model

class Size(DateTimeModel):
    name = models.CharField(max_length=250)
    
    class Meta:
        verbose_name = ('Size')
        verbose_name_plural = ('Sizes')
        ordering = ['-name']

    def __str__(self):
        return self.name

#Product Image Model

class ProductImage(DateTimeModel):
    image = models.ImageField(upload_to="products")
    
    # class Meta:
    #     verbose_name = ('ProductImage')
    #     verbose_name_plural = ('ProductImages')

    # def __str__(self):
    #     return self.name

#Product Model

class Products(DateTimeModel):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    brands = models.ForeignKey(Brands, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ManyToManyField(ProductImage)
    description = RichTextField()
    size= models.ManyToManyField(Size)
    price = models.PositiveIntegerField()
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, primary_key=True)
    vat_incl = models.BooleanField(default=False)
    vat_percent = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank= True)
    vat_amt = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank= True)
    discount_percent=models.DecimalField(max_digits=12, decimal_places=2, null=True, blank= True)
    discount_amt =  models.DecimalField(max_digits=12, decimal_places=2, null=True, blank= True)
    view_count = models.PositiveIntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name = ('Product')
        verbose_name_plural = ('Products')
        ordering = ['-name']

    def __str__(self):
        return self.name
    

#Coupon Model

class Coupon(DateTimeModel):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    valid_to = models.DateTimeField(null=True, blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=250)
    discount_percent = models.DecimalField(
        null=True, max_digits=12, decimal_places=2)
    discount_amt = models.DecimalField(
        null=True, max_digits=12, decimal_places=2)
    discount_type = models.CharField(null=True, max_length=40, choices=TYPE)
    is_used = models.BooleanField(default=False, null=True, blank= True)
    validity_count = models.PositiveIntegerField(default= 1)

    class Meta:
        verbose_name = ('Coupon')
        verbose_name_plural = ('Coupons')
        ordering = ['-title']

    def __str__(self):
        return "Coupon code: " + self.code

#Order Model
 
class Order(DateTimeModel):
    code = models.CharField(max_length=50, unique=True )
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ManyToManyField(Products)
    shipping_address = models.CharField(max_length=200)
    billing_address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(null=True, blank=True)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=ORDER_STATUS)
    payment_method = models.CharField(max_length=20, choices=METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(default=False, null=True, blank=True)
    
    class Meta:
        verbose_name = ('Order')
        verbose_name_plural = ('Orders')
        ordering = ['-status']
        
    def __str__(self):
        return "Order: " + self.code
