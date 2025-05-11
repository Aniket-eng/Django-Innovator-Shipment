from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.


class RoleModel(models.Model):
    role_id = models.IntegerField(primary_key=True,blank=False)
    role_Name = models.CharField(max_length=15,default='user',blank=False,null=False)



class UserModel(AbstractBaseUser):
    id = models.IntegerField(primary_key=True,null=False,unique=True)
    userName = models.CharField(max_length=150,unique=True)
    email = models.EmailField(null=False,unique=True)
    password = models.CharField(max_length=100)
    user_role = models.ForeignKey(RoleModel,on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    

class ShipmentModel(models.Model):
    shipment_id = models.IntegerField(primary_key=True,auto_created=True)
    shipment_category = models.CharField(max_length=25)
    country = models.CharField(max_length=20)
    status = models.CharField(max_length=500,default='yet to be shipped',blank=True)
    transanctionNumber = models.IntegerField(unique=True)
    date = models.DateField(default=datetime.date(datetime.today()),blank=True)
    role = models.ForeignKey(RoleModel,on_delete=models.CASCADE)
    subject_id = models.ForeignKey(UserModel,on_delete=models.CASCADE)

