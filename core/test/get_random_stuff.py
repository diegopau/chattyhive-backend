from core.test.text_generator.random_generator import Generator
from core.test.name_generator import names
from core.test.category_generator.choose_category import choose_random_category
from core.test.text_generator.hive_name_generator import create_hive_name
import random
import hashlib
import time
from django.utils import timezone
from uuid import uuid4
import string
from datetime import datetime
from core.test.predefined_tags import predefined_unique_tags, predefined_non_unique_tags


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

# This is for get_random_email() method
domains = ["hotmail.com", "gmail.com", "aol.com", "mail.com", "mail.kz", "yahoo.com"]

SECRET_KEY = 'asd538J878hdfjKEidrfdgf0954lKUJMd03l4mfjejJKkek4AA'

try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    import warnings
    warnings.warn('A secure pseudo-random number generator is not available '
                  'on your system. Falling back to Mersenne Twister.')
    using_sysrandom = False


def __string_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Returns a securely generated random string.

    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits
    """
    if not using_sysrandom:
        # This is ugly, and a hack, but it makes things better than
        # the alternative of predictability. This re-seeds the PRNG
        # using a value that is hard for an attacker to predict, every
        # time a random string is required. This may change the
        # properties of the chosen random sequence slightly, but this
        # is better than absolute predictability.
        random.seed(
            hashlib.sha256(
                ("%s%s%s" % (
                    random.getstate(),
                    time.time(),
                    SECRET_KEY)).encode('utf-8')
            ).digest())
    return ''.join(random.choice(chars) for _ in range(size))


def get_random_email():
    if not using_sysrandom:
        random.seed(
            hashlib.sha256(
                ("%s%s%s" % (
                    random.getstate(),
                    time.time(),
                    SECRET_KEY)).encode('utf-8')
            ).digest())
    # Not all the possibilities are taking into account:
    local_part = string.ascii_lowercase + string.ascii_uppercase + string.digits + "#-_~!$&'()*+,;=:"

    email = ''
    while True:
        # Django demands a maximum of 75 chars for EmailField, this is a limitation of Django Framework
        # If we need more we should look at the consecuences of raising this to 254 (estándar)

        if len(email) < 75:
            email = ''.join(random.choice(local_part) for _ in range(random.randint(1, 50))) + '@' + random.choice(domains)
            break
    print("Chosen email: ", email)
    return email


def get_random_date():
    year = random.randint(2014, 2015)

    if year == 2015:
        month = random.randint(1, 3)
    else:
        month = random.randint(1, 12)

    if month == 2:
        day = random.randint(1, 28)
    else:
        day = random.randint(1, 30)

    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    microsecond = random.randint(0, 999999)

    random_date = datetime(year, month, day, hour, minute, second, microsecond, tzinfo=timezone.get_default_timezone())
    return random_date


# probability defines de probability of having a totally random tag or a predefined tag
def get_random_tag(probability=30):
    if random.randrange(100) < probability:
        # The higher percent value is, the more likely it will get into this part of the if else
        tag = __string_generator(size=random.randint(1, 32),
                                 chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + '_')
    else:
        tag = random.choice(predefined_unique_tags)
        predefined_unique_tags.remove(tag)
    return tag


def get_random_tags(quantity=random.randint(1, 5), probability=40):
    tags = []
    for tag in range(0, quantity):
        if random.randrange(100) < probability:
            # The higher percent value is, the more likely it will get into this part of the if else
            tags[tag] = __string_generator(size=random.randint(1, 32),
                                           chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + '_')
        else:
            tags[tag] = random.choice(predefined_non_unique_tags)
    return tags


def get_random_hive_name():
    return create_hive_name()


def get_random_hive_priority():
    return random.randint(1, 100)


def get_random_public_name():
    return __string_generator(size=random.randint(1, 20),
                              chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + '_')


def get_random_username():
    return uuid4().hex[:30]


def get_random_category_code():
    return choose_random_category()


def get_random_full_name(gender):
    return names.get_full_name(gender)


def get_random_hive_description():
    # Because we don't always want long names we change the relative maximum length of the description
    max_length = random.randint(100, 2048)
    random_description = ''
    last_paragraph = ''
    while len(random_description) < (max_length + 1):
        last_paragraph = generator.get_paragraphs(1)[0]
        print("last_paragraph es de tipo")
        type(last_paragraph)
        print("last_paragraph: ", last_paragraph)
        random_description += last_paragraph + '\n'
    random_description = random_description[0:(len(random_description) - (len(last_paragraph) + 1))]
    return random_description