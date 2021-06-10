from django.views import generic
from rest_framework import generics

from django.shortcuts import render

from dashboard.models import *
from dashboard.mixin import NonDeletedItemMixin
from .serializers import *
# Create your views here.

# product api


class ProductListCreate(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers


# class ProductUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializers

# category api


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialize


class CategoryUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialize

# brand api


class BrandListCreate(NonDeletedItemMixin, generics.ListCreateAPIView):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializers


class BrandUpdateDelete(NonDeletedItemMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializers

# coupon api
class CouponListCreate(generics.ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializers


class CouponUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializers

# size api

class SizeListCreate(NonDeletedItemMixin, generics.ListCreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializers


class SizeUpdateDelete(NonDeletedItemMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializers


# customer api
class CustomerListCreate(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers


class CustomerUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers