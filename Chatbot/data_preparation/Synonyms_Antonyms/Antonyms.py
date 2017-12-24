# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 11:59:10 2016

@author: Gayatri.k
"""

##### Antonyms #####

from nltk.corpus import wordnet as wn

def replace(word, pos=None):
    antonyms = set()
    for syn in wn.synsets(word, pos=pos):
      for lemma in syn.lemmas():
        for antonym in lemma.antonyms():
          antonyms.add(antonym.name())
    if len(antonyms) == 1:
      return antonyms.pop()
    else:
      return None


def replace_negations(sent):
    i, l = 0, len(sent)
    words = []
    while i < l:
      word = sent[i]
      if word == 'not' and i+1 < l:
        ant = replace(sent[i+1])
        if ant:
          words.append(ant)
          i += 2
          continue
      words.append(word)
      i += 1
    return words