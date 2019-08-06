from django.db import models

from django.contrib.auth.models import User

import datetime

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class Address(models.Model):
    address = models.CharField(max_length=50)

    def __str__(self):
        return self.address

class Phone(models.Model):
    phone = models.CharField(
        max_length=15)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return self.phone + "-" + self.address.address

class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError('Users must have an email address')

        elif not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(models.Model):

    #user = models.OneToOneField(User, on_delete=models.CASCADE,)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    slogan = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    bio = models.CharField(max_length=350)
    #profile_pic = models.ImageField(upload_to='Profile/Picture/')
    date = models.DateTimeField(auto_now_add=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    address = models.ManyToManyField(Address)
    phone = models.ManyToManyField(Phone)
    
    def __str__(self):
        return self.username


class Connection(models.Model):
    follower = models.ForeignKey(User, related_name='Cliente', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='Proveedor', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(
            self.follower.username,
            self.following.username
            )
