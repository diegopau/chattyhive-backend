# coding=utf-8
__author__ = 'xurxo'

from django.test import TestCase
from core.models import ChUser, ChUserManager, ChProfile, ChHive, ChChat, ChSubscription


class UserTestCase(TestCase):
    def setUp(self):
        ChUser.objects.create(username="one@a.com")
        ChUser.objects.create(username="two@a.com")
        ChProfile.objects.create(user=ChUser.objects.get(username="one@a.com"))
        ChProfile.objects.create(user=ChUser.objects.get(username="two@a.com"))

    def test_User_info(self):
        """         """
        oneUser = ChUser.objects.get(username="one@a.com")
        twoUser = ChUser.objects.get(username="two@a.com")
        one = ChProfile.objects.get(user=oneUser)
        two = ChProfile.objects.get(user=twoUser)
        one.set_public_name("One")
        one.set_first_name("One First Name")
        one.set_last_name("One Last Name")
        one.set_language("en-gb")
        one.set_location("London, England")
        one.set_sex("Male")
        one.set_show_location(True)
        one.set_public_show_age(False)
        one.set_private_show_age(True)
        two.set_public_name("Two")
        two.set_first_name("Two First Name")
        two.set_last_name("Two Last Name")
        two.set_language("es-es")
        two.set_location("Madrid, España")
        two.set_sex("Female")
        two.set_show_location(False)
        two.set_public_show_age(True)
        two.set_private_show_age(True)