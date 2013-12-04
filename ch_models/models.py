__author__ = 'xurxo'

from django.db import models

class User(models.Model):
    username = models.CharField(max_length=16)
    email = models.EmailField()

class Profile(models.Model):
    public_name = models.CharField(max_length=24)
    name = models.CharField(max_length=24)
    surname = models.CharField(max_length=48)
    age = models.BigIntegerField
    sex = models.CharField
    description = models.CharField(max_length=160)

class Subscription(models.Model):
    type = models.CharField
    user = User
    if type=="chat":
        chattyhive = Chat
    else:
        chattyhive = Hive

class Hive(models.Model):
    type = models.CharField

class Chat(models.Model):
    type = models.CharField

class Basic_Message(models.Model):
    type = models.CharField