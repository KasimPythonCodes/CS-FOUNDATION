from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid
# Create your models here.

class CUMMONID(models.Model):
    id = models.UUIDField(primary_key=True ,editable=False , unique=True , default = uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    class Meta:
        abstract =True

class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to="Admin/Upload", height_field=None, width_field=None, max_length=None)
    def __str__(self):
        return str(self.username)

class User_Contact_Info(CUMMONID):
    full_name = models.CharField(max_length=20, blank=True ,null=True)
    user_email = models.EmailField(max_length=120, blank=True ,null=True)
    phone_no = models.CharField(max_length=20, blank=True ,null=True)
    subject = models.CharField(max_length=50, blank=True ,null=True)
    message_info = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=False, auto_now=True,null=True,blank=True)  
    

    def __str__(self):
        return self.full_name
    


class Image_Category(models.Model):
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    create_category=models.CharField(max_length=120 ,blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=False, auto_now=True,null=True,blank=True)  
    

    def __str__(self):
        return str(self.create_category)    


class Admin_Post_Img(models.Model):
    Img_Avatar = models.ImageField(upload_to = 'ADMIN/IMAGE')
    select_category=models.ForeignKey(Image_Category, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.select_category.create_category)


class Evant(models.Model):
    img_evant = models.ImageField(upload_to='Evant')
    def __str__(self):
        return str(self.id)
    
                              