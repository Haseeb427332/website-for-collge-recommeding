from django.db import models
from django.contrib import admin
from clg_finder.models import *
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import post_save
#from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.sessions.models import Session

class user_data23(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(unique = True,error_messages ={ 
                    "unique":"User with this Email ID is already exists"
                    })
    username = models.CharField(max_length = 20)
    last_name = models.CharField(max_length= 20)
    password = models.CharField(max_length = 20000)
    Phone_no = models.CharField(max_length=10,null=True,unique=True,error_messages ={ 
                    "unique":"User with this Phone number is already exists"
                    } )
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    Rdate = models.DateTimeField(auto_now_add=True,null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True,null=True)
    staff_clg_code = models.IntegerField(default=None,null=True)
    instu_code = models.IntegerField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    profile_pic = models.ImageField(upload_to = 'pictures/')
    objects = UserManager()

class favourites(models.Model):
    user_id = models.IntegerField()
    fav_college_id = models.IntegerField()
    