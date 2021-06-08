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
