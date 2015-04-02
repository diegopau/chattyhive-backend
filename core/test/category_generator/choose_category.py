"""Using the categories.txt gets a random category

"""
from random import randint


categories_txt = open("categories.txt")
categories = categories_txt.read().split()
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

