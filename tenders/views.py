from django.shortcuts import render
import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import requests
# Create your views here.
from rest_framework import mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from tenders import models
from tenders import serializers
# Create your views here.
class CategoryView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Returns a list of all location records
        """
        return self.list(request, *args, **kwargs)
class StructureView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Structure.objects.all()
    serializer_class = serializers.StructureSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Returns a list of all location records
        """
        return self.list(request, *args, **kwargs)
class ProfileView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Returns a list of all location records
        """
        return self.list(request, *args, **kwargs)
    def post(self,request, *args, **kwargs):
        print(request)
        print(request.data)
        print(request.query_params)
        return Response('Успешно.', status.HTTP_202_ACCEPTED)
class TendersView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Tenders.objects.all()
    serializer_class = serializers.TendersSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Returns a list of all location records
        """
        return self.list(request, *args, **kwargs)
    def post(self,request, *args, **kwargs):
        print(request)
        print(request.data)
        print(request.query_params)
        return Response('Успешно.', status.HTTP_202_ACCEPTED)
class OrdersView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Orders.objects.all()
    serializer_class = serializers.OrdersSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Returns a list of all location records
        """
        return self.list(request, *args, **kwargs)
    def post(self,request, *args, **kwargs):
        print(request)
        print(request.data)
        print(request.query_params)
        return Response('Успешно.', status.HTTP_202_ACCEPTED)