from random import randint
import os

file_path = os.path.join(os.path.dirname(__file__), 'random_english_words.txt')
english_words_txt = open(file_path)
english_words = english_words_txt.read().split()
number_of_words = len(english_words)
print("Number of english words: ", number_of_words)


def create_hive_name():
    # Because we don't always want long names we change the relative maximum length of the name
    max_length = randint(25, 80)
    hive_name = ''
    last_word = ''
    while len(hive_name) < (max_length + 1):
        selected = randint(1, number_of_words)
        last_word = english_words[selected]
        hive_name += last_word + ' '
    hive_name = hive_name[0:(len(hive_name)-(len(last_word)+2))]
    # In category we have a string that is a line from categories.txt, now we split that line in four and we take the
    # third param that is the code.
    print("Chosen hive name: ", hive_name)
    return hive_name