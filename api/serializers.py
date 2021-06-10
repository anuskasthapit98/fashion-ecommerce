from rest_framework import serializers
from dashboard.models import *


# category 
class CategorySerialize(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

# product
class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

# brand
class BrandSerializers(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'

# coupon
class CouponSerializers(serializers.ModelSerializer):

    valid_to = serializers.DateField
    valid_from = serializers.DateField
    
    class Meta:
        model = Coupon
        fields = '__all__'

# size
class SizeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['name']

# coupon
class CustomerSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Customer
        fields = '__all__'