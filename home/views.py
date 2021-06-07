from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins

from dashboard.models import *
from .serializers import ProductSerializers
# Create your views here.


class ProductApiView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin):
    serializer_class = ProductSerializers
    queryset = Products.objects.filter(deleted_at__isnull=True)
    lookup_fields = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)


class ProductApiIdview(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = ProductSerializers
    queryset = Products.objects.filter(deleted_at__isnull=True)
    lookup_fields = 'id'

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)
