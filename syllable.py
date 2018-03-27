# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:27:40 2018

Space is limited
In a haiku, so it's hard
To finish what you

@author: tpaye
"""

# import nltk
# nltk.download('cmudict')
# nltk.download('wordnet')

from nltk.corpus import cmudict
from nltk.corpus import wordnet as wn
import pyphen
import re, string
from gensim.models import KeyedVectors

#%%
# load the Stanford GloVe model
filename = 'glove.6B.50d.txt.word2vec'
model = KeyedVectors.load_word2vec_format(filename, binary=False)

print('Done loading model')
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
        return len(pyphen_dict.inserted(word).split('-'))


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


def get_synonyms(word, w2v):
    ret_syns = []
    if w2v:
        synonyms = model.most_similar(word, topn=10)
        for synonym in synonyms:
            ret_syns.append(synonym[0])
    else:
        for ss in wn.synsets(word):
            ret_syns += ss.lemma_names()
    while '.' in ret_syns:
        ret_syns.remove('.')
    while ',' in ret_syns:
        ret_syns.remove(',')
    while '?' in ret_syns:
        ret_syns.remove('?')
    if len(ret_syns) > 10:
        return ret_syns[:10]
    return ret_syns


def make_length_n(words, n):
    m = syl_in_words(words)
    new_words = words[:]
    w2v = False
    while m != n:
        for i, word in enumerate(words):
            word = word.lower()
            new_word = word
            synonyms = get_synonyms(word, w2v)
            for synonym in synonyms:
                if n < m and nsyl(synonym) < nsyl(word):
                    new_word = synonym
                    break
                elif n > m and nsyl(synonym) > nsyl(word):
                    new_word = synonym
                    break
            new_words[i] = new_word
            if new_word != word:
                m += nsyl(new_word) - nsyl(word)
        if words == new_words:
            if w2v:
                return False
            else:
                # fall back to word2vec
                w2v = True
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
            first_half.append(w)
    return first_half, second_half


def cut_thirds(ws):
    first_third = []
    second_third = []
    third_third = []
    n = syl_in_words(ws)
    m = 0
    for w in ws:
        m += nsyl(w)
        if m < n/3:
            first_third.append(w)
        elif m > 2*(n/3):
            third_third.append(w)
        else:
            second_third.append(w)
    return first_third, second_third, third_third


def modify_words(words, b, m, e):
    bws = []
    mws = []
    ews = []
    if b and m:
        ews = make_length_n(cut_off(words, 12), 5)
        bws = cut_out(words, 12)
    elif e and m:
        bws = make_length_n((cut_off(reversed(words), 12))[::-1], 5)
        ews = (cut_out(reversed(words), 12))[::-1]
    elif b and e:
        mws = make_length_n(cut_off(reversed(cut_off(reversed(words), 5)), 5), 7)
        bws = cut_out(words, 5)
        ews = (cut_out(reversed(words), 5))[::-1]
    elif b:
        mws, ews = cut_half(cut_off(words, 5))
        mws = make_length_n(mws, 7)
        ews = make_length_n(ews, 5)
        bws = cut_out(words, 5)
    elif e:
        mws, bws = cut_half(cut_off(reversed(words), 5))
        bws = bws[::-1]
        mws = mws[::-1]
        bws = make_length_n(bws, 5)
        mws = make_length_n(mws, 7)
        ews = (cut_out(reversed(words), 12))[::-1]
    else:
        bws, mws, ews = cut_thirds(words)
        bws = make_length_n(bws, 5)
        mws = make_length_n(mws, 7)
        ews = make_length_n(ews, 5)
    if bws is False or mws is False or ews is False:
        return ["Alas, it seems I can't make a haiku out of what you have written."]
    return bws + mws + ews


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
    elif syl_in_sentence(sentence) < 13:
        return format_haiku("The text you wrote me seems excessively short for making a haiku")
    else:
        return format_haiku("The text you wrote me seems excessively long for making a haiku")


def nvowels(word):
    ys = 0
    for i, l in enumerate(word):
        if l == 'y':
            front = False
            if i != 0:
                if word[i-1] not in "aeiou":
                    front = True
            if front and i < len(word):
                if word[i-1] not in "aeiou":
                    ys += 1
    return ys + sum(map(word.lower().count, "aeiou"))


def clappify(sentence):
    clapped = ""
    for word in sentence.split(' '):
        if nsyl(word) == nvowels(word):
            # every vowel-letter is a vowel-sound
            # we can clap that
            clapped_word = ""
            claps = 0
            for i, l in enumerate(word):
                clapped_word += l
                if l in "aeiou":
                    if i < len(word):
                        if claps < nvowels(word)-1:
                            clapped_word += "👏"
                            claps += 1
                elif l == 'y':
                    # check whether y is a vowel
                    front = False
                    if i != 0:
                        if word[i-1] not in "aeiou":
                            front = True
                    if front and i < len(word):
                        if word[i-1] not in "aeiou":
                            # y is a vowel
                            if claps < nvowels(word)-1:
                                clapped_word += "👏"
                                claps += 1
            clapped += clapped_word + "👏"
        else:
            for syl in pyphen_dict.inserted(word).split('-'):
                clapped += syl + "👏"
        clapped += " "
    return clapped[:-1]


def main():
    pass

if __name__ == '__main__':
    main()
