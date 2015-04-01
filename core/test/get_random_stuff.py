from core.test.text_generator.random_generator import Generator
from core.test.name_generator.names import
from random import randint

with open('data/sample.txt', 'r') as sample_txt:
    sample = sample_txt.read()
with open('data/dictionary.txt', 'r') as dictionary_txt:
    dictionary = dictionary_txt.read().split()

generator = Generator(sample, dictionary)

def get_random_tag():



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


def get_random_hive_description():
    random_description = generator.generate_paragraphs(randint(1, 3))
    return random_description