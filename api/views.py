from django.shortcuts import render
from rest_framework import generics

from dashboard.models import *
from .serializers import *
# Create your views here.


class ProductListCreate(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers


class ProductUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers


class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerialize


class CategoryUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brands.objects.all()
    serializer_class = CategorySerialize


class BrandListCreate(generics.ListCreateAPIView):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializers


class BrandUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brands.objects.all()
    serializer_class = BrandSerializers