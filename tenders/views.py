import datetime

from django.db.models import Q
import json

from django.conf import settings
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
        if request.user.profile.role!= models.UserRole.MODERATOR:
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
            user= models.User.objects.get(email=request.data['user_email'])
        else:
            user = request.user
        full_name=request.data['full_name']
        phone=request.data['phone']
        structure= models.Structure.objects.get(id=int(request.data['structure']))
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
        if role== models.UserRole.CUSTOMER:
            queryset = queryset.filter(
                Q(customer=user)
                | Q(executor=user)
            ).distinct()
        elif role== models.UserRole.MODERATOR:
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
        category= models.Category.objects.get(id=int(request.query_params['category']))
        new_tender= models.Tenders()
        new_tender.category=category
        new_tender.name=request.query_params['name']
        new_tender.enable=True
        new_tender.customer=request.user
        new_tender.save()
        print(request.data)
        if 'document' in request.data:
            print(request.data['document'])
            tender_file= models.TendersFile()
            tender_file.tender=new_tender
            tender_file.file=request.data['document']
            tender_file.save()

        if 'document2' in request.data:
            print(request.data['document2'])
            tender_file= models.TendersFile()
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
            tender.status= models.TenderStatus.ON_APPROVE
            tender.moderator_complate=True
            tender.date_start=datetime.datetime.now()
            tender.date_end=datetime.datetime.now()+datetime.timedelta(days=1)
            tender.save()
            if models.TGUsers.objects.filter(user=tender.customer).exists():
                tg_user= models.TGUsers.objects.get(user=tender.customer)
                text = f'Изменен статус Тендера <b>{tender.id}</b> \n' \
                       f'Статус : <b>{tender.status}</b>\n'

                data = {
                    'text': (None, text),
                    'chat_id': (None, tg_user.chat_id),
                    'parse_mode': (None, 'HTML'),
                    # 'reply_markup': (None, new_kb)
                }
                res = requests.post(url=settings.TELEGRAM_SEND_URL, headers={}, files=data)
                print(res)
            res = {'text': 'Тендер успешно одобрен.', 'tender_id': tender.id}
            return Response(res, status.HTTP_202_ACCEPTED)
        elif command=='REJECTED':
            tender_id = request.data['tender_id']
            reject_text = request.data['reject_text']
            tender = models.Tenders.objects.get(id=int(tender_id))
            tender.reject_text = reject_text
            tender.enable = False
            tender.status= models.TenderStatus.REJECTED
            tender.save()
            if models.TGUsers.objects.filter(user=tender.customer).exists():
                tg_user= models.TGUsers.objects.get(user=tender.customer)
                text = f'Изменен статус Тендера <b>{tender.id}</b> \n' \
                       f'Статус : <b>{tender.status}</b>\n' \
                       f'Причина : <b>{tender.reject_text}</b>\n'

                data = {
                    'text': (None, text),
                    'chat_id': (None, tg_user.chat_id),
                    'parse_mode': (None, 'HTML'),
                    # 'reply_markup': (None, new_kb)
                }
                res = requests.post(url=settings.TELEGRAM_SEND_URL, headers={}, files=data)
                print(res)
            res = {'text': 'Тендер успешно отклонен.', 'tender_id': tender.id}
            return Response(res, status.HTTP_202_ACCEPTED)
class OrdersView(mixins.ListModelMixin, GenericAPIView):
    queryset = models.Orders.objects.all()
    serializer_class = serializers.OrdersSerializer
    pagination_class = None
    def get_queryset(self):
        tender_id=self.request.query_params['tender_id']
        tender= models.Tenders.objects.get(id=int(tender_id))
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
        tender= models.Tenders.objects.get(id=int(tender_id))
        user=request.user
        order= models.Orders()
        order.tender=tender
        order.executor=user
        order.price=price
        order.save()
        return Response('Заявка успешно добавлено.', status.HTTP_202_ACCEPTED)


class OrdersCheckView(mixins.ListModelMixin, GenericAPIView):
    def get(self, request, *args, **kwargs):
        user=request.user
        tender_id =request.query_params['tender_id']
        tender= models.Tenders.objects.get(id=int(tender_id))
        if tender.winner:
            if tender.winner==user:
                return Response({'status': 'winner'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'no_loser'}, status=status.HTTP_200_OK)
        else:
            if models.Orders.objects.filter(tender=tender, executor=user).exists():
                return Response({'status': 'in_progress'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'created'}, status=status.HTTP_200_OK)


class TenderCheckView(mixins.ListModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        from django.utils import timezone
        now = timezone.now()
        tenders= models.Tenders.objects.filter(enable=True).exclude(status=models.TenderStatus.FINISHED).exclude(status=models.TenderStatus.REJECTED).exclude(status=models.TenderStatus.NO_ACTIVE)

        print('now=',now)
        for i in tenders:
            if i.date_end:
                if now>i.date_end:
                    orders= models.Orders.objects.filter(tender=i).order_by('price')
                    if len(orders)>0:
                        i.order=orders[0]
                        i.executor=orders[0].executor
                        i.winner=orders[0].executor
                        i.status= models.TenderStatus.FINISHED
                        i.save()
                        if models.TGUsers.objects.filter(user=i.customer).exists():
                            tg_user = models.TGUsers.objects.get(user=i.customer)
                            text = f'Выявлен победитель Тендера <b>{i.id}</b> \n' \
                                   f'Название <b>"{i.name}"</b>\n' \
                                   f'Описание: <b>{i.description}</b>\n' \
                                   f'Статус : <b>{i.status}</b>\n' \
                                   f'Выиграл: <b>{i.winner.profile.full_name}</b>\n' \
                                   f'Телефонный номер: <b>{i.winner.profile.phone}</b>\n' \
                                   f'Цена: <b>{i.order.price}</b>'

                            data = {
                                'text': (None, text),
                                'chat_id': (None, tg_user.chat_id),
                                'parse_mode': (None, 'HTML'),
                                # 'reply_markup': (None, new_kb)
                            }
                            res = requests.post(url=settings.TELEGRAM_SEND_URL, headers={}, files=data)
                            print(res)
                        if models.TGUsers.objects.filter(user=i.winner).exists():
                            tg_user = models.TGUsers.objects.get(user=i.winner)
                            text = f'Вы победитель Тендера <b>{i.id}</b> \n' \
                                   f'Название <b>"{i.name}"</b>\n' \
                                   f'Описание: <b>{i.description}</b>\n' \
                                   f'Заказчик: <b>{i.customer.profile.full_name}</b>\n'\
                                   f'Телефонный номер: <b>{i.customer.profile.phone}</b>\n'\
                                   f'Статус : <b>{i.status}</b>\n' \
                                   f'Цена: <b>{i.order.price}</b>'

                            data = {
                                'text': (None, text),
                                'chat_id': (None, tg_user.chat_id),
                                'parse_mode': (None, 'HTML'),
                                # 'reply_markup': (None, new_kb)
                            }
                            res = requests.post(url=settings.TELEGRAM_SEND_URL, headers={}, files=data)
                            print(res)
                    else:
                        i.status= models.TenderStatus.NO_ACTIVE
                        i.save()
                        if models.TGUsers.objects.filter(user=i.customer).exists():
                            tg_user = models.TGUsers.objects.get(user=i.customer)
                            text = f'Не выявлен победитель Тендера <b>{i.id}</b> \n' \
                                   f'Название <b>"{i.name}"</b>\n' \
                                   f'Описание: <b>{i.description}</b>\n' \
                                   f'Статус : <b>{i.status}</b>\n' \
                                   f'Заявки не найдены по тендеру\n' \

                            data = {
                                'text': (None, text),
                                'chat_id': (None, tg_user.chat_id),
                                'parse_mode': (None, 'HTML'),
                                # 'reply_markup': (None, new_kb)
                            }
                            res = requests.post(url=settings.TELEGRAM_SEND_URL, headers={}, files=data)
                            print(res)


            # if i.date_end<datetime.datetime.now():
            #     print(i.id)
        return Response({'status': 'created'}, status=status.HTTP_200_OK)



class CheckUserByChatIDView(mixins.ListModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        print(request.data)
        chat_id=request.data['chat_id']
        command=request.data['command']
        if models.TGUsers.objects.filter(chat_id=chat_id).exists():
            menu = []
            tg_user= models.TGUsers.objects.get(chat_id=chat_id)
            role=tg_user.user.profile.role
            if role == models.UserRole.CUSTOMER:
                menus = [
                    ["📘Мои тендера"],
                    ["📙Активные тендеры"],
                ]
            elif models.UserRole.EXECUTOR:
                menus = [
                    ["📘Мои заявки"],
                    ["📙Активные заявки"],
                ]
            else:
                menus = [
                ]
            def get_role(role):
                if role == models.UserRole.CUSTOMER:
                    return 'Заказчик'
                elif models.UserRole.EXECUTOR:
                    return 'Исполнитель'
                else:
                    return 'Модератор'
            for i in menus:
                menu.append(i)
            new_kb = json.dumps({"keyboard": menu})

            data = {
                'text': (None, f'Добро пожаловать <b>{tg_user.user.profile.full_name}</b>!Ваша роль в системе {get_role(role)}!'),
                'chat_id': (None, chat_id),
                'parse_mode': (None, 'HTML'),
                'reply_markup': (None, new_kb)
            }
            if command == "start":
                res = requests.post(url=settings.TELEGRAM_SEND_URL, headers={}, files=data)
            return Response({'status': True,'role':role}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False}, status=status.HTTP_200_OK)

class CheckUser(mixins.ListModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        print(request.data)
        email=request.data['email']
        print(email)
        if models.User.objects.filter(email=email).exists():
            user= models.User.objects.get(email=email)
            if models.TGUsers.objects.filter(user=user).exists():
                return Response({'status': False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'status': True}, status=status.HTTP_200_OK)
        else:
            return Response({'status': False}, status=status.HTTP_200_OK)

class AppendTGUser(mixins.ListModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        print(request.data)
        try:
            email=request.data['email']
            user= models.User.objects.get(email=email)
            chat_id=request.data['chat_id']
            tg_user= models.TGUsers()
            tg_user.chat_id=chat_id
            tg_user.user=user
            tg_user.save()
            role=user.profile.role
            menu=[]
            if role == models.UserRole.CUSTOMER:
                menus = [
                    ["📘Мои тендера"],
                    ["📙Активные тендеры"],
                ]
            elif models.UserRole.EXECUTOR:
                menus = [
                    ["📘Мои заявки"],
                    ["📙Активные заявки"],
                ]
            else:
                menus = [
                    ["📤Сообщить о нарушении"],
                    ["📗Выданные указания"],
                    ["📕Просроченные указания"],
                    ["📒Неназначенные заявки"],
                    ["📙Все указания"],
                    ["📕Отклоненные заявки"],
                    ["📘Мои заявки"],
                    ["🔙Назад"],
                ]
            def get_role(role):
                if role == models.UserRole.CUSTOMER:
                    return 'Заказчик'
                elif models.UserRole.EXECUTOR:
                    return 'Исполнитель'
                else:
                    return 'Модератор'
            for i in menus:
                menu.append(i)
            new_kb = json.dumps({"keyboard": menu})

            data = {
                'text': (None, f'Добро пожаловать <b>{tg_user.user.profile.full_name}</b>!Ваша роль в системе {get_role(role)}!'),
                'chat_id': (None, chat_id),
                'parse_mode': (None, 'HTML'),
                'reply_markup': (None, new_kb)
            }
            res = requests.post(url=settings.TELEGRAM_SEND_URL, headers={}, files=data)
            return Response({'status': True,'role':role}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': e}, status=status.HTTP_200_OK)

class Customer_TG(mixins.ListModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        print(request.data)
        chat_id=request.data['chat_id']
        command_name=request.data['command_name']
        tg_user= models.TGUsers.objects.get(chat_id=chat_id)
        user=tg_user.user
        if command_name=='📘Мои заявки':
            tenders= models.Tenders.objects.filter(orders__executor=user, enable=True).distinct()
            print(tenders)
            for tender in tenders:
                date_start = tender.date_start.strftime("%d-%m-%Y, %H:%M:%S")
                date_end = tender.date_end.strftime("%d-%m-%Y, %H:%M:%S")
                if tender.winner == user:

                    text=f'Тендер <b>{tender.id}</b> \n' \
                         f'Название <b>"{tender.name}"</b>\n'\
                         f'Дата начало: <b>{date_start}</b>\n' \
                         f'Дата завершение: <b>{date_end}</b>\n'\
                         f'Описание: <b>{tender.description}</b>\n'\
                         f'Заказчик: <b>{tender.customer.profile.full_name}</b>\n'\
                         f'Статус : <b>{tender.status}</b>\n'\
                         f'Выиграл: <b>{tender.winner.profile.full_name}</b>\n' \
                         f'Цена: <b>{tender.order.price}</b>'
                else:
                    text = f'Тендер  <b>{tender.id}</b> \n'\
                           f'Название: <b>"{tender.name}"</b>\n'\
                           f'Дата начало: <b> {date_start}</b>\n'\
                           f'Дата завершение: <b> {date_end}</b>\n'\
                           f'Описание: <b>{tender.description}</b>'\
                           f'Заказчик: <b>{tender.customer.profile.full_name}</b>\n'\
                           f'Статус : <b>{tender.status}</b>'
                data = {
                    'text': (None, text),
                    'chat_id': (None, chat_id),
                    'parse_mode': (None, 'HTML'),
                    # 'reply_markup': (None, new_kb)
                }
                res = requests.post(url=settings.TELEGRAM_SEND_URL, headers={}, files=data)
                print(res)
                print(res.json())
        elif command_name=='📙Активные заявки':
            tenders= models.Tenders.objects.filter(winner=user, enable=True).distinct()
            print(tenders)
            for tender in tenders:
                if tender.winner == user:

                    text=f'Тендер <b>{tender.id}</b> \n' \
                         f'Название <b>"{tender.name}"</b>\n'\
                         f'Описание: <b>{tender.description}</b>\n'\
                         f'Заказчик: <b>{tender.customer.profile.full_name}</b>\n'\
                         f'Телефонный номер: <b>{tender.customer.profile.phone}</b>\n'\
                         f'Статус : <b>{tender.status}</b>\n'\
                         f'Выиграл: <b>{tender.winner.profile.full_name}</b>\n' \
                         f'Цена: <b>{tender.order.price}</b>'
                else:
                    text = f'Тендер  <b>{tender.id}</b> \n'\
                           f'Название: <b>"{tender.name}"</b>\n'\
                           f'Описание: <b>{tender.description}</b>'\
                           f'Заказчик: <b>{tender.customer.profile.full_name}</b>\n'\
                           f'Статус : <b>{tender.status}</b>'
                data = {
                    'text': (None, text),
                    'chat_id': (None, chat_id),
                    'parse_mode': (None, 'HTML'),
                    # 'reply_markup': (None, new_kb)
                }
                res = requests.post(url=settings.TELEGRAM_SEND_URL, headers={}, files=data)
                print(res)
                print(res.json())
        return Response({'status': True}, status=status.HTTP_200_OK)
class EXECUTOR_TG(mixins.ListModelMixin, GenericAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        print(request.data)
        chat_id=request.data['chat_id']
        command_name=request.data['command_name']
        tg_user = models.TGUsers.objects.get(chat_id=chat_id)
        user=tg_user.user
        if command_name=='📘Мои тендера':
            tenders= models.Tenders.objects.filter(customer=user, enable=True).distinct()
            print(tenders)
            for tender in tenders:
                if tender.winner :

                    text=f'Тендер <b>{tender.id}</b> \n' \
                         f'Название <b>"{tender.name}"</b>\n'\
                         f'Описание: <b>{tender.description}</b>\n'\
                         f'Статус : <b>{tender.status}</b>\n'\
                         f'Выиграл: <b>{tender.winner.profile.full_name}</b>\n' \
                         f'Телефонный номер: <b>{tender.winner.profile.phone}</b>\n' \
                         f'Цена: <b>{tender.order.price}</b>'
                else:
                    text = f'Тендер  <b>{tender.id}</b> \n'\
                           f'Название: <b>"{tender.name}"</b>\n'\
                           f'Описание: <b>{tender.description}</b>'\
                           f'Статус : <b>{tender.status}</b>'
                data = {
                    'text': (None, text),
                    'chat_id': (None, chat_id),
                    'parse_mode': (None, 'HTML'),
                    # 'reply_markup': (None, new_kb)
                }
                res = requests.post(url=settings.TELEGRAM_SEND_URL, headers={}, files=data)
                print(res)
                print(res.json())
        elif command_name=='📙Активные тендеры':
            tenders= models.Tenders.objects.filter(winner__isnull=False, enable=True).distinct()
            print(tenders)
            for tender in tenders:
                text=f'Тендер <b>{tender.id}</b> \n' \
                         f'Название <b>"{tender.name}"</b>\n'\
                         f'Описание: <b>{tender.description}</b>\n'\
                         f'Статус : <b>{tender.status}</b>\n'\
                         f'Выиграл: <b>{tender.winner.profile.full_name}</b>\n' \
                         f'Телефонный номер: <b>{tender.winner.profile.phone}</b>\n' \
                         f'Цена: <b>{tender.order.price}</b>'

                data = {
                    'text': (None, text),
                    'chat_id': (None, chat_id),
                    'parse_mode': (None, 'HTML'),
                    # 'reply_markup': (None, new_kb)
                }
                res = requests.post(url=settings.TELEGRAM_SEND_URL, headers={}, files=data)
                print(res.json())
        return Response({'status': True}, status=status.HTTP_200_OK)