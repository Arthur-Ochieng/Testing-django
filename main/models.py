from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    user_type_data = ((1, "SuperAdmin"), (2, "SaccoAdmin"), (3, "Members"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class SuperAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class SaccoAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()



class Saccos(models.Model):
    id = models.AutoField(primary_key=True)
    sacco_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.sacco_name


class Members(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    sacco_id = models.ForeignKey(Saccos, on_delete=models.DO_NOTHING, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


#Creating Django Signals
 
# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            SuperAdmin.objects.create(admin=instance)
        if instance.user_type == 2:
            SaccoAdmin.objects.create(admin=instance)
        if instance.user_type == 3:
            Members.objects.create(admin=instance, course_id=Saccos.objects.get(id=1), address="", profile_pic="", gender="")
    
 
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.superadmin.save()
    if instance.user_type == 2:
        instance.saccoadmin.save()
    if instance.user_type == 3:
        instance.members.save()

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)        
# def create_auth_toke(sender, instance=None,created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

