# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:27:40 2018

Space is limited
In a haiku, so it's hard
To finish what you

@author: tpaye
"""

from nltk.corpus import cmudict
import pyphen
import re, string

cmu_dict = cmudict.dict()
pyphen_dict = pyphen.Pyphen(lang='en')

# counts the syllables in a word. (might make some mistakes)
# https://stackoverflow.com/questions/405161/detecting-syllables-in-a-word
# https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word
def nsyl(word):
    try:
        # list comprehensions make code more redable :^)
        return [len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word.lower()]][0] # [0] takes the first one if the word can be pronounced in multiple ways
    except KeyError:
        return len(pyphen_dict.inserted('Whitecaps').split('-'))


# counts number of syllables in sentence
def has_right_num_syl(sentence):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    sentence = regex.sub('', sentence)
    words = sentence.split()
    counter = 0
    for word in words:
        counter += nsyl(word)
    return counter == 17

# A Haiku is a short poem with 17 syllables aranged in a 5-7-5 pattern
def crappy_haiku(sentence):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    sentence = regex.sub('', sentence)
    if has_right_num_syl(sentence) is not True:
        return False
    words = sentence.split()
    sub_counter = 0
    for idx, word in enumerate(words):
        sub_counter += nsyl(word)
        
        

#print(nsyl("schiffahrt"))
print(cmu_dict["spider"])
print(nsyl('spider'))

#%%
def count_sylable_per_word(sentence):
    words = sentence.split()
    for word in words:
        print(word, " ", nsyl(word))