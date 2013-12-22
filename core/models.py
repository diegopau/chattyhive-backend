__author__ = 'lorenzo'

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class ChUserManager(UserManager):
    def create_user(self, username, email, password, *args, **kwargs):
        print('user')
        print(username)
        print('email')
        print(email)
        print('pass')
        print(password)
        user = ChUser(username=username)    #TODO it works, but, it's correct?
        user.email = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ChUser(AbstractUser):
    ##****************Key Fields****************#
    # username = AbstractUser
    # email = AbstractUser
    #****************Info Fields****************#
    # first_name = AbstractUser
    # last_name = AbstractUser
    birth_date = models.DateField(null=True, auto_now=False, auto_now_add=False)
    # sex =
    # language =
    # timezone =
    #****************Control Fields****************#
    is_authenticated = models.BooleanField(default=False)

    objects = ChUserManager()

    # REQUIRED_FIELDS = ['email', 'Name', 'LastName']
    USERNAME_FIELD = 'username'

    # def get_full_name(self):
    #     return "% % %"(self.username)

    # def get_short_name(self):
    #     return "% % %"(self.username)

    def is_authenticated(self):
        return AbstractUser.is_authenticated(self)