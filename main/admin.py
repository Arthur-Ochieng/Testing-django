from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main.models import *

class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel),
admin.site.register(SuperAdmin),
admin.site.register(SaccoAdmin),
admin.site.register(Saccos),
admin.site.register(Members),



# Register your models here.
