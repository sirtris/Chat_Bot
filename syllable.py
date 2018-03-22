# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 10:27:40 2018

@author: tpaye
"""

from nltk.corpus import cmudict
d = cmudict.dict()

# https://stackoverflow.com/questions/405161/detecting-syllables-in-a-word
def nsyl(word):
  return [(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]] 

print(nsyl("schiffahrt"))
print(d["project"])