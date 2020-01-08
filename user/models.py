from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


# Customized user model e.g. for register and login by e-mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from mysite import settings


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, is_staff=False, is_active=True,
                    is_admin=False):  # creting our user
        if not email:
            raise ValueError("Users must have an email adress")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)  # change user password
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    phone_number = models.IntegerField(null=True)
    room_number = models.TextField(null=True)
    consultations = models.TextField(null=True)

    USERNAME_FIELD = 'email'  # assigning an email as a username
    REQUIRED_FIELDS = ['first_name', 'last_name']  # set as necessary for filling

    objects = UserManager()  # user is create by UserManager

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property  # it changes the field value dynamically, we define the value as a method but we are able to access like an attribute, works similar to seter in java
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)