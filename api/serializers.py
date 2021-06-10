from rest_framework import serializers
from dashboard.models import *
import datetime

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

class CouponSerializers(serializers.ModelSerializer):

    valid_to = serializers.DateField
    valid_from = serializers.DateField
    
    class Meta:
        model = Coupon
        fields = '__all__'

class SizeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['name']
