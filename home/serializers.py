from rest_framework import serializers
from dashboard.models import Products


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        depth = 1
