__author__ = 'diego'

# -*- coding:utf-8 -*-

# Core Django imports
from django.test import TestCase
from django.conf.global_settings import LANGUAGES
from core import models

# Third-party app imports
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key


class ChUserTestModel(TestCase):
    def setUp(self):
        self.users = mommy.make_recipe('core.user', _quantity=100)

    def test_user_creation(self):
        for user in self.users:
            print("user name: ", user.username)
        assert len(self.users) == 100


class TagModelTestModel(TestCase):

    def setUp(self):
        self.tags = mommy.make_recipe('core.tag', _quantity=150)

    def test_tag_creation(self):
        for tag in self.tags:
            print("tag name: ", tag.tag)
        assert len(self.tags) == 150


class LanguageModelTestModel(TestCase):

    def setUp(self):
        languages = []
        for lang in LANGUAGES:
            # language es una tupla con dos valores, se coge el primer valor
            languages.append(mommy.make(models.LanguageModel, language=lang[0]))
        for lang in languages:
            print("language code: ", lang.language)
        assert len(languages)


class ChHiveTestModel(TestCase):

    def setUp(self):
        self.hives = mommy.make_recipe('core.hive', _quantity=50)

    def test_hive_creation(self):
        for hive in self.hives:
            print("hive name: ", hive.name)
            print("hive description: ", hive.description)
            for tag in hive.tags:
                print("hive tag: ", tag.tag)
        assert len(self.hives) == 50