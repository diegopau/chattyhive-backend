from core.test.text_generator.random_generator import Generator
from core.test.name_generator import names
from random import randint, random
import string


##########################################################
# THIS IS FOR RANDOM BIG TEXT (random_generator package) #
##########################################################

with open('data/sample.txt', 'r') as sample_txt:
    sample = sample_txt.read()
with open('data/dictionary.txt', 'r') as dictionary_txt:
    dictionary = dictionary_txt.read().split()

generator = Generator(sample, dictionary)
##########################################################


def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_random_tag():
    return string_generator(size=randint(1, 32), chars=string.ascii_uppercase + string.ascii_lowercase + '_')


# def get_random_hive_name():
#
#
# def get_random_public_name():
#
#
# def get_random_username():
#
#
# def get_random_category_code():


def get_random_full_name(gender):
    names.getfull_name(gender)


def get_random_hive_description():
    random_description = generator.generate_paragraphs(randint(1, 3))
    return random_description