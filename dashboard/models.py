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
    subCategory = models.ForeignKey('self', on_delete=models.CASCADE)

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')

    def __str__(self):
        return self.name

# class SubCategory(TimeStamp):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE )
#     name= models.CharField(max_length=250)
#     img = models.ImageField(upload_to="subcategory")

#     class Meta:
#         verbose_name = ('SubCategory')
#         verbose_name_plural = ('SubCategories')

#     def __str__(self):
#         return self.name


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
    discount = models.PositiveIntegerField()
    view_count = models.PositiveIntegerField(default=0)

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
