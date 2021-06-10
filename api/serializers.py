from rest_framework import serializers
from dashboard.models import *


class CategorySerialize(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'


class SizeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['name']
