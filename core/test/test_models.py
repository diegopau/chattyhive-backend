__author__ = 'diego'

# -*- coding:utf-8 -*-

#Core Django imports
from django.test import TestCase

#Third-party app imports
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key


class TagModelTestModel(TestCase):
    def setUp(self):
        self.tags = mommy.make_recipe('core.tag', _quantity=20)

    def test_tag_creation(self):
        for tag in self.tags:
            print("tag name: ", tag.tag)

        assert len(self.tags) == 25
