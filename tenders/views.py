import datetime

from django.db.models import Q
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

class TenderView(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    queryset = models.Tenders.objects.all()
    serializer_class = serializers.TendersSerializer
    pagination_class = None

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class TendersView(mixins.ListModelMixin, GenericAPIView):
    # queryset = models.Tenders.objects.all()
    serializer_class = serializers.TendersSerializer
    pagination_class = None
    def get_queryset(self):

        queryset = models.Tenders.objects.all()
        user = self.request.user
        profile=user.profile
        role=profile.role
        if role==models.UserRole.CUSTOMER:
            queryset = queryset.filter(
                Q(customer=user)
                | Q(executor=user)
            ).filter(enable=True).distinct()
        else:
            queryset = queryset.filter(
                Q(customer=user)
                | Q(executor=user)
            ).distinct()
        return queryset
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self,request, *args, **kwargs):
        category=models.Category.objects.get(id=int(request.query_params['category']))
        new_tender=models.Tenders()
        new_tender.category=category
        new_tender.name=request.query_params['name']
        new_tender.enable=True
        new_tender.customer=request.user
        new_tender.save()
        if 'document' in request.data:
            tender_file=models.TendersFile()
            tender_file.tender=new_tender
            tender_file.file=request.data['document']
            tender_file.save()
        res={'text':'Тендер успешно создано.','tender_id':new_tender.id}
        return Response(res, status.HTTP_202_ACCEPTED)
    def put(self,request, *args, **kwargs):
        user = self.request.user
        command=request.data['command']
        if command=='SUCCESS':
            tender_id = request.data['tender_id']
            description = request.data['description']
            tender = models.Tenders.objects.get(id=int(tender_id))
            tender.description=description
            tender.status=models.TenderStatus.ON_APPROVE
            tender.moderator_complate=True
            tender.date_start=datetime.datetime.now()
            tender.date_end=datetime.datetime.now()+datetime.timedelta(days=1)
            tender.save()
            res = {'text': 'Тендер успешно одобрен.', 'tender_id': tender.id}
            return Response(res, status.HTTP_202_ACCEPTED)
        elif command=='REJECTED':
            tender_id = request.data['tender_id']
            reject_text = request.data['reject_text']
            tender = models.Tenders.objects.get(id=int(tender_id))
            tender.reject_text = reject_text
            tender.enable = False
            tender.status=models.TenderStatus.REJECTED
            tender.save()
            res = {'text': 'Тендер успешно отклонен.', 'tender_id': tender.id}
            return Response(res, status.HTTP_202_ACCEPTED)
class OrdersView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Orders.objects.all()
    serializer_class = serializers.OrdersSerializer
    pagination_class = None
    def get_queryset(self):
        tender_id=self.request.query_params['tender_id']
        tender=models.Tenders.objects.get(id=int(tender_id))
        queryset = models.Orders.objects.all()
        user = self.request.user
        queryset = queryset.filter(
            tender=tender)
        return queryset
    def get(self, request, *args, **kwargs):
        """
        Returns a list of all location records
        """
        return self.list(request, *args, **kwargs)
    def post(self,request, *args, **kwargs):
        tender_id=request.data['tender_id']
        price=request.data['price']
        tender=models.Tenders.objects.get(id=int(tender_id))
        user=request.user
        order=models.Orders()
        order.tender=tender
        order.executor=user
        order.price=price
        order.save()
        return Response('Заявка успешно добавлено.', status.HTTP_202_ACCEPTED)


class OrdersCheckView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Orders.objects.all()
    serializer_class = serializers.OrdersSerializer
    pagination_class = None
    def get(self, request, *args, **kwargs):
        user=request.user
        try:
            order=models.Orders.objects.get(executor=user)
            return Response({'order_id':order.id},status=status.HTTP_200_OK)
        except:
            return Response('Не найдено', status=status.HTTP_404_NOT_FOUND)