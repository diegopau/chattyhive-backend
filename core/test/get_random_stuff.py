from core.test.text_generator.random_generator import Generator
from core.test.name_generator import names
from core.test.category_generator.choose_category import choose_random_category
from random import randint, random, choice
from uuid import uuid4
import string
from core.models import ChCategory


##########################################################
# THIS IS FOR RANDOM BIG TEXT (random_generator package) #
##########################################################

with open('data/sample.txt', 'r') as sample_txt:
    sample = sample_txt.read()
with open('data/dictionary.txt', 'r') as dictionary_txt:
    dictionary = dictionary_txt.read().split()

generator = Generator(sample, dictionary)
##########################################################


def __string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(choice(chars) for _ in range(size))


def get_random_tag():
    return __string_generator(size=randint(1, 32), chars=string.ascii_uppercase + string.ascii_lowercase + '_')


def get_random_hive_name():


def get_random_public_name():
    return __string_generator(size=randint(1, 20), chars=string.ascii_uppercase + string.ascii_lowercase + '_')


def get_random_username():
    return uuid4().hex[:30]

def get_random_category_code():
    return choose_random_category()

def get_random_full_name(gender):
    return names.get_full_name(gender)


def get_random_hive_description():
    random_description = generator.generate_paragraphs(randint(1, 3))
    return random_description