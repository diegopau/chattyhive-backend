"""Using the categories.txt gets a random category

"""
from random import randint
import os

file_path = os.path.join(os.path.dirname(__file__), 'categories.txt')
categories_txt = open(file_path)
categories = categories_txt.read().split('\n')
number_of_categories = len(categories)
print("Number of categories: ", number_of_categories)


def choose_random_category():
    selected = randint(1, number_of_categories)
    category = categories[selected]

    # In category we have a string that is a line from categories.txt, now we split that line in four and we take the
    # third param that is the code.
    code = category.split(':')[3]
    print("Chosen category code: ", code)
    return code