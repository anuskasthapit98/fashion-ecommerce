from rest_framework import serializers
from .models import *

class BrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Brands
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    # brands = BrandSerializer()
    class Meta:
        model = Products
        fields = ['slug', 'name', 'brands','categories','price','discount','status','view_count']
        depth = 1
