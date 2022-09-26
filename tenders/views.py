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
        if request.user.profile.role!=models.UserRole.MODERATOR:
            return Response('Пошел на хуй', status.HTTP_202_ACCEPTED)

        def get_role(text):
            if text == 'MODERATOR':
                return models.UserRole.MODERATOR
            elif text == 'CUSTOMER':
                return models.UserRole.CUSTOMER
            elif text == 'EXECUTOR':
                return models.UserRole.EXECUTOR

        email = request.data['email']
        if models.User.objects.filter(email=email).exists():
            return Response('В базе данных уже существует пользователь с таким email', status.HTTP_202_ACCEPTED)

        user = models.User()
        password = request.data['password']
        full_name = request.data['full_name']
        phone = request.data['phone']
        structure = models.Structure.objects.get(id=int(request.data['structure']))
        print(request.data['role'])
        role = get_role(request.data['role'])
        user.email = email
        user.set_password(password)

        profile = models.Profile()
        profile.full_name = full_name
        profile.phone = phone
        profile.structure = structure
        profile.role = role
        profile.user = user
        user.save()
        profile.save()
        return Response('Успешно добавлен.', status.HTTP_202_ACCEPTED)
    def put(self,request,*args, **kwargs):
        def get_role(text):
            if text=='"MODERATOR"':
                return models.UserRole.MODERATOR
            elif text=='CUSTOMER':
                return models.UserRole.CUSTOMER
            elif text=='EXECUTOR':
                return models.UserRole.EXECUTOR


        if 'user_email' in request.data:
            user=models.User.objects.get(email=request.data['user_email'])
        else:
            user = request.user
        full_name=request.data['full_name']
        phone=request.data['phone']
        structure=models.Structure.objects.get(id=int(request.data['structure']))
        role=get_role(request.data['role'])
        profile=user.profile
        profile.full_name=full_name
        profile.phone=phone
        profile.structure=structure
        profile.role=role
        profile.user=user
        profile.save()
        return Response('Успешно изменен!.', status.HTTP_202_ACCEPTED)
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
            ).distinct()
        elif role==models.UserRole.MODERATOR:
            queryset = queryset.all()
        else:
            queryset = queryset.filter(
                Q(enable=True)
                | Q(moderator_complate=True)
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
        print(request.data)
        if 'document' in request.data:
            print(request.data['document'])
            tender_file=models.TendersFile()
            tender_file.tender=new_tender
            tender_file.file=request.data['document']
            tender_file.save()

        if 'document2' in request.data:
            print(request.data['document2'])
            tender_file=models.TendersFile()
            tender_file.tender=new_tender
            tender_file.file=request.data['document2']
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
    def get(self, request, *args, **kwargs):
        user=request.user
        tender_id =request.query_params['tender_id']
        tender=models.Tenders.objects.get(id=int(tender_id))
        if tender.winner:
            if tender.winner==user:
                return Response({'status': 'winner'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'no_loser'}, status=status.HTTP_200_OK)
        else:
            if models.Orders.objects.filter(tender=tender,executor=user).exists():
                return Response({'status': 'in_progress'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'created'}, status=status.HTTP_200_OK)


class TenderCheckView(mixins.ListModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        from django.utils import timezone
        now = timezone.now()
        tenders=models.Tenders.objects.filter(enable=True).exclude(status=models.TenderStatus.FINISHED).exclude(status=models.TenderStatus.REJECTED).exclude(status=models.TenderStatus.NO_ACTIVE)

        print('now=',now)
        for i in tenders:
            if i.date_end:
                if now>i.date_end:
                    orders=models.Orders.objects.filter(tender=i).order_by('price')
                    if len(orders)>0:
                        i.order=orders[0]
                        i.executor=orders[0].executor
                        i.winner=orders[0].executor
                        i.status=models.TenderStatus.FINISHED
                        i.save()
                    else:
                        i.status=models.TenderStatus.NO_ACTIVE
                        i.save()


            # if i.date_end<datetime.datetime.now():
            #     print(i.id)
        return Response({'status': 'created'}, status=status.HTTP_404_NOT_FOUND)
