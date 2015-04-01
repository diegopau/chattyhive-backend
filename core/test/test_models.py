__author__ = 'diego'

# -*- coding:utf-8 -*-

#Core Django imports
from django.test import TestCase

#Third-party app imports
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

# Relative imports of the 'app-name' package
from core.models import TagModel


class TagModelTestModel(TestCase):
    def setUp(self):
        self.tag = mommy.make(TagModel)
