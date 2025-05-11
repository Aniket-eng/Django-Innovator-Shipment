from django.contrib import admin
from .models import UserModel,ShipmentModel,RoleModel
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(UserModel)
admin.site.register(RoleModel)
admin.site.register(ShipmentModel)