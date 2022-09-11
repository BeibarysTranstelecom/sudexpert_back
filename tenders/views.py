import datetime

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
class ProfileDetailView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TendersView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Tenders.objects.all()
    serializer_class = serializers.TendersSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        """
        Returns a list of all location records
        """
        return self.list(request, *args, **kwargs)
    def post(self,request, *args, **kwargs):
        category=models.Category.objects.get(id=request.query_params['category'])
        new_tender=models.Tenders()
        new_tender.category=category
        new_tender.name=request.query_params['name']
        new_tender.date_start=datetime.datetime.today()
        new_tender.date_end=datetime.datetime.today()+datetime.timedelta(days=1)
        new_tender.enable=True
        new_tender.customer=request.user
        new_tender.save()
        tender_file=models.TendersFile()
        tender_file.tender=new_tender
        tender_file.file=request.data['document']
        tender_file.save()
        res={'text':'Тендер успешно создано.','tender_id':new_tender.id}
        return Response(res, status.HTTP_202_ACCEPTED)
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