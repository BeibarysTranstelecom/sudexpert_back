from rest_framework import serializers
from rest_framework.serializers import ValidationError
from tenders import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"
class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Structure
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    structure=StructureSerializer(read_only=True)
    class Meta:
        model = models.Profile
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = models.User
        fields = ["id", "email", "profile"]

class TenderFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TendersFile
        fields = "__all__"
class TendersSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    customer = UserSerializer(read_only=True)
    executor = UserSerializer(read_only=True)
    files = TenderFileSerializer(read_only=True,many=True)
    class Meta:
        model = models.Tenders
        fields = ['id','name','category','date_start', 'date_end','status','description',
                  'reject_text','moderator_complate','enable','customer',
                  'winner','order','files','executor']
class OrdersSerializer(serializers.ModelSerializer):
    tender=TendersSerializer(read_only=True)
    executor = UserSerializer(read_only=True)
    class Meta:
        model = models.Orders
        fields = "__all__"