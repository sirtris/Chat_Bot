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
from gensim.models import KeyedVectors
#%%
# load the Stanford GloVe model
filename = 'glove.6B.50d.txt.word2vec'
model = KeyedVectors.load_word2vec_format(filename, binary=False)
#%%
cmu_dict = cmudict.dict()
pyphen_dict = pyphen.Pyphen(lang='en')

def remove_punctuation(s):
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    return regex.sub('', s)


# counts the syllables in a word. (might make some mistakes)
# https://stackoverflow.com/questions/405161/detecting-syllables-in-a-word
# https://datascience.stackexchange.com/questions/23376/how-to-get-the-number-of-syllables-in-a-word
def nsyl(word):
    word = remove_punctuation(word).lower()
    if word == "":
        return 0
    try:
        # list comprehensions make code more redable :^)
        return [len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word]][0] # [0] takes the first one if the word can be pronounced in multiple ways
    except KeyError:
        return len(pyphen_dict.inserted('Whitecaps').split('-'))


# counts number of syllables in sentence
def syl_in_words(words):
    counter = 0
    for word in words:
        counter += nsyl(word)
    return counter

# counts number of syllables in sentence
def syl_in_sentence(sentence):
    sentence = remove_punctuation(sentence)
    words = sentence.split()
    return syl_in_words(words)


def beginning_is_n_syllables(words, n):
    sub_counter = 0
    for word in words:
        sub_counter += nsyl(word)
        if sub_counter == n:
            return True
        elif sub_counter > n:
            return False

def words_to_sentence(ws):
    s = ""
    for w in ws:
        s += w + " "
    return s[:-1]

# A Haiku is a short poem with 17 syllables aranged in a 5-7-5 pattern
def is_haiku(sentence):
    if syl_in_sentence(sentence) != 17:
        return False
    sentence = remove_punctuation(sentence)
    words = sentence.split()
    sub_counter = 0
    line_counter = 0
    for word in words:
        sub_counter += nsyl(word)
        if sub_counter == 5 + ((line_counter % 2) * 2):
            sub_counter = 0
            line_counter += 1
    return line_counter == 3

# when you give a sentece(haiku) the function formats it
def format_haiku(sentence):
    if is_haiku(sentence):
        haiku = ""
        if syl_in_sentence(sentence) != 17:
            return False
        words = sentence.split()
        sub_counter = 0
        for word in words:
            haiku += word
            sub_counter += nsyl(word)
            if sub_counter == 5 or sub_counter == 12:
                haiku += "\n"
            else:
                haiku += " "
        return haiku[:-1]
    else:
        return "Not a Haiku: " + sentence

def cut_off(words, n):
    sub_counter = 0
    short_words = []
    for word in words:
        sub_counter += nsyl(word)
        if sub_counter > n:
            short_words.append(word)
    return short_words
            
def cut_out(words, n):
    sub_counter = 0
    short_words = []
    for word in words:
        sub_counter += nsyl(word)
        short_words.append(word)
        if sub_counter == n:
            return short_words            

def make_length_n(words, n):
    m = syl_in_words(words)
    new_words = words[:]
    while m != n:
        for i, word in enumerate(words):
            word = word.lower()
            new_word = word
            synonyms = model.most_similar(word, topn=10)
            for synonym in synonyms:
                synonym = synonym[0]
                if n < m and nsyl(synonym) < nsyl(word):
                    new_word = synonym
                    break
                elif n > m and nsyl(synonym) > nsyl(word):
                    new_word = synonym
                    break
            new_words[i] = new_word
            if new_word != word:
                m += nsyl(new_word) - nsyl(word)
        words = new_words[:]
    return new_words


def cut_half(ws):
    first_half = []
    second_half = []
    n = syl_in_words(ws)
    m = 0
    for w in ws:
        m += nsyl(w)
        if m > n/2:
            second_half.append(w)
        else:
            first_half(w)
    return first_half, second_half


def modify_words(words, b, m, e):
    if b and m:
        return cut_out(words, 12) + make_length_n(cut_off(words, 12), 5)
    elif e and m:
        return make_length_n(reversed(cut_off(reversed(words), 12), 5)) + (cut_out(reversed(words), 12))[::-1]
    elif b and e:
        return cut_out(words, 5) + make_length_n(cut_off(reversed(cut_off(reversed(words), 5)), 5), 7) + (cut_out(reversed(words), 5))[::-1]
    elif b:
        mws, ews = cut_half(cut_off(words, 5))
        return cut_out(words, 5) + make_length_n(mws, 7) + make_length_n(ews, 5)
    elif e:
        mws, bws = cut_half(cut_off(reversed(words), 5))
        bws = bws[::-1]
        mws = mws[::-1]
        return make_length_n(bws, 5) + make_length_n(mws, 7) + (cut_out(reversed(words), 12))[::-1]
    elif m:
        return ["middle", "fits"]
    else:
        return ["nothing", "fits"]


def generate_haiku(sentence):
    if is_haiku(sentence):
        return format_haiku(sentence)
    # gatekeeping
    if syl_in_sentence(sentence) in range(13, 22):
        end_okay, middle_okay, beginning_okay = False, False, False
        sentence = remove_punctuation(sentence)
        words = sentence.split()
        beginning_okay = beginning_is_n_syllables(words, 5)
        end_okay = beginning_is_n_syllables(reversed(words), 5)
        if not (end_okay and beginning_okay):
            if beginning_okay == end_okay:
                #check for middle?
                pass
            elif end_okay:
                middle_okay = beginning_is_n_syllables(reversed(words), 12)
            else:
                middle_okay = beginning_is_n_syllables(words, 12)
        # else: middle_okay = False
        words = modify_words(words, beginning_okay, middle_okay, end_okay)
        return format_haiku(words_to_sentence(words))
    else:
        return "This is too long or too short to be a Haiku"