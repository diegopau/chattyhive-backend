from core.test.text_generator.random_generator import Generator
from core.test.name_generator import names
from core.test.category_generator.choose_category import choose_random_category
from core.test.text_generator.hive_name_generator import create_hive_name
from random import randint, choice
from uuid import uuid4
import string
from core.models import ChCategory


##########################################################
# THIS IS FOR RANDOM BIG TEXT (random_generator package) #
##########################################################
import os

file_path1 = os.path.join(os.path.dirname(__file__), 'text_generator/default/sample.txt')
file_path2 = os.path.join(os.path.dirname(__file__), 'text_generator/default/dictionary.txt')

with open(file_path1, 'r') as sample_txt:
    sample = sample_txt.read()
with open(file_path2, 'r') as dictionary_txt:
    dictionary = dictionary_txt.read().split()

generator = Generator(sample, dictionary)
##########################################################


def __string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(choice(chars) for _ in range(size))


def get_random_tag():
    tag = __string_generator(size=randint(1, 32), chars=string.ascii_uppercase + string.ascii_lowercase + '_')
    print("New Tag!: ", tag)
    return tag


def get_random_hive_name():
    return create_hive_name()


def get_random_public_name():
    return __string_generator(size=randint(1, 20), chars=string.ascii_uppercase + string.ascii_lowercase + '_')


def get_random_username():
    return uuid4().hex[:30]


def get_random_category_code():
    return choose_random_category()


def get_random_full_name(gender):
    return names.get_full_name(gender)


def get_random_hive_description():
    # Because we don't always want long names we change the relative maximum length of the description
    max_length = randint(100, 2048)
    random_description = ''
    last_paragraph = ''
    while len(random_description) < (max_length + 1):
        last_paragraph = generator.generate_paragraphs(1)
        random_description += last_paragraph + '\n'
    random_description = random_description[0:(len(random_description)-(len(last_paragraph)+1))]
    return random_description