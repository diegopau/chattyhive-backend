from model_mommy.recipe import Recipe, foreign_key
from core.models import ChHive, TagModel, ChUser
from core.test import get_random_stuff
import random

# We define here the structure of the tag, then in test_models.py we generate a lot of them

user = Recipe(
    ChUser,
    date_joined=get_random_stuff.get_random_date,
    email=get_random_stuff.get_random_email,
    username=get_random_stuff.get_random_username,
)


tag = Recipe(
    TagModel,
    tag=get_random_stuff.get_random_tag,
)


hive = Recipe(
    ChHive,
    category=get_random_stuff.get_random_category_code,
    creation_date=get_random_stuff.get_random_date,
    creator=foreign_key(user),
    description=get_random_stuff.get_random_hive_description,
    priority=get_random_stuff.get_random_hive_priority,
    name=get_random_stuff.get_random_hive_name,

    # The model layer should decide if create a new tag (if it didn't exist) or get existing tag (establish
    # many-to-many relationship)
    tags=get_random_stuff.get_random_tags,
)