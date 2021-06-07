from rest_framework import serializers
from dashboard.models import *


class CategorySerialize(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = "__all__"
        
        
