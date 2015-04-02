from model_mommy.recipe import Recipe
from core.models import ChHive, TagModel
from core.test import get_random_stuff

# We define here the structure of the tag, then in test_models.py we generate a lot of them
tag = Recipe(
    TagModel,
    tag=get_random_stuff.get_random_tag(),
)