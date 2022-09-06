from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import gettext_lazy as _

from tenders.managers import UserManager


class TenderStatus(models.TextChoices):
    CREATED = "CREATED", _("Создано")
    ON_APPROVE = "ON_APPROVE", _("На согласовании")
    FINISHED = "FINISHED", _("Завершено")
    REJECTED = "REJECTED", _("Отклонено")

class UserRole(models.TextChoices):
    MODERATOR = "MODERATOR", _("Модератор")
    CUSTOMER = "CUSTOMER", _("Заказчик")
    EXECUTOR = "EXECUTOR", _("Исполнитель")

class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = None
    last_name = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        try:
            return self.profile.full_name
        except ObjectDoesNotExist:
            raise

class Structure(models.Model):
    name = models.CharField(_("Название "), max_length=255)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name ='Структура'
        verbose_name_plural='Структура'

class Profile(models.Model):
    user_directory_path = "user/profile/"
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE, related_name="profile"
    )
    full_name = models.CharField(_("ФИО"), max_length=150)
    role = models.CharField(
        choices=UserRole.choices, default=UserRole.EXECUTOR,verbose_name='Роль',max_length=255
    )
    phone = models.CharField(max_length=255,verbose_name='Телефонный номер')
    date_regist = models.DateField(auto_now_add=True)
    structure=models.ForeignKey(Structure,on_delete=models.PROTECT,verbose_name='Структура')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.full_name
    class Meta:
        verbose_name ='Профиль'
        verbose_name_plural='Профиль'
        ordering=['-date_regist']

# Create your models here.
class Category(models.Model):
    name = models.CharField(_("Название категорий"), max_length=255)
    models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name ='Категория'
        verbose_name_plural='Категория'
        ordering=['-id']

class Tenders(models.Model):
    name = models.CharField(_("Название тендера"), max_length=255)
    category=models.ForeignKey(Category,on_delete=models.PROTECT,verbose_name='Категория')
    date_start=models.DateField(blank=True,null=True)
    date_end=models.DateField(blank=True,null=True)
    date_created=models.DateField(auto_now_add=True)
    status=models.CharField(
        choices=TenderStatus.choices, default=TenderStatus.CREATED,verbose_name='Статус',max_length=255
    )
    moderator_complate=models.BooleanField(default=False,verbose_name='Проверка модератора')
    enable=models.BooleanField(default=False,verbose_name='Активный')
    customer=models.ForeignKey(User,on_delete=models.SET_NULL,verbose_name='Заказчик',related_name='tender_customer',null=True,blank=True)
    executor=models.ForeignKey(User,on_delete=models.SET_NULL,verbose_name='Исполнитель',related_name='tender_executor',null=True,blank=True)
    order=models.ForeignKey('Orders',on_delete=models.SET_NULL,verbose_name='Победитель',related_name='tender_order',null=True,blank=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name ='Тендеры'
        verbose_name_plural='Тендеры'
        ordering=['-id']

class Orders(models.Model):
    tender=models.ForeignKey(Tenders,on_delete=models.PROTECT,verbose_name='Тендер',related_name='orders')
    executor=models.ForeignKey(User,on_delete=models.PROTECT,verbose_name='Исполнитель',related_name='order_executors')
    price=models.IntegerField(verbose_name='Цена')
    date_created=models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.id} заявка на тендер {self.tender.id}'
    class Meta:
        verbose_name ='Заявки'
        verbose_name_plural='Заявки'
        ordering=['-id']

