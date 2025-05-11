from rest_framework import serializers
from .models import ShipmentModel,RoleModel,UserModel
from django.contrib.auth import get_user_model
from datetime import datetime
'''
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['user_role','password','email','username']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self,validated_data):
        #user_name = validated_data['user_name']
        password = validated_data['password']
        user_role = validated_data['user_role']
        email = validated_data['email']
        user = get_user_model()
        username = validated_data['username']
        new_user = user.objects.create(user_role=user_role,email=email,username=username)
        new_user.set_password(password)
        new_user.save()
        return new_user
    
'''

class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email','password']

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentModel
        fields = '__all__'

class PostShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentModel
        fields = ['shipment_category','transanctionNumber','country','status','date']

    def validate(self,data):
        if data.get('status',None)==None or len(data.get('status',None)) <1:
            data['status'] = 'yet to be shipped'
        if data.get('date',None)==None:
            data['date'] = datetime.date(datetime.today())
        return data
