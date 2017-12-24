# -*- coding: utf-8 -*-
"""
Created on Mon Aug 01 14:51:10 2016

@author: Gayatri.k, Sharda.sinha
"""

###### Preprocessing functionalities #######

# Importing packages
import nltk
from nltk.stem.snowball import SnowballStemmer
import re
import collections
import dill
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath('__file__')))))

import config as cfg

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    list_pd = ["&quot;", "&bull;", "&amp;", "&lt;", "&gt;", "&nbsp;", "&iexcl;", "&cent;",  "&pound;", "&curren;", "&yen;", "&brvbar;", "&sect;", "&uml;", "&copy;", "&ordf;", "&laquo;", "&not;", "&shy;", "&reg;", "&macr;", "&deg;", "&plusmn;", "&sup2", "&sup3;", "&acute;", "&micro;", "&para;", "&middot;", "&cedil;", "&sup1;", "&ordm;", "&raquo;", "&frac14;", "&frac12;", "&frac34;", "&iquest;", "&times;", "&divide;", "&ETH;", "&eth;", "&THORN;", "&thorn;", "&AElig;", "&aelig;", "&OElig;", "&oelig;", "&Aring;", "&Oslash;", "&Ccedil;", "&ccedil;", "&szlig;", "&Ntilde;", "&ntilde;"]
    for rem in list_pd:
        cleantext= cleantext.replace(rem, ' ')
    return cleantext.strip()

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()


# Data preparation
def data_prep(text, company_name, stem=True, remove_stopwords=True, check_spellings = True):
    # data_prep_path = cfg.ROOT + '/data_preparation/Data_prep/'
    data_prep_path = cfg.ROOT + '/data_preparation/vocab/' + company_name +"/"
    with open(data_prep_path + 'spell_model', 'rb') as in_strm:
        NWORDS = dill.load(in_strm)

    def words(data):
        return re.findall('[a-zA-Z0-9]+', data.lower())

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    stemmer = SnowballStemmer("english", ignore_stopwords=True)

    # text_file = open(data_prep_path + 'discover_keywords.txt', 'r')
    # filtered_keywords = text_file.read().split('\n')

    def edits1(word):
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
        replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
        inserts = [a + c + b for a, b in splits for c in alphabet]
        return set(deletes + transposes + replaces + inserts)

    def known_edits2(word):
        return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

    def known(words):
        return set(w for w in words if w in NWORDS)

    def correct(word):
        candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
        return max(candidates, key=NWORDS.get)

    def spell_check(text):
        words = (text.split())
        correct_words = []
        for i in words:
            correct_words.append(correct(i))
        return correct_words

    if check_spellings:
        refined_text = spell_check(text.lower())
        refined_text = ' '.join(refined_text)
    else:
        refined_text = text

    def stopword_removal(tokens):
        stopwords = nltk.corpus.stopwords.words('english')
        tokens = [w for w in tokens if not w in stopwords]
        return tokens

    # Tokenising and stemming
    def tokenize_and_stem(refined_text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(refined_text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z0-9]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        if remove_stopwords:
            stems = stopword_removal(stems)
        return stems

    # Tokenising
    def tokenize_only(refined_text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word.lower() for sent in nltk.sent_tokenize(refined_text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z0-9]', token):
                filtered_tokens.append(token)
        if remove_stopwords:
            filtered_tokens = stopword_removal(filtered_tokens)
        return filtered_tokens

    if stem:
        token_output = tokenize_and_stem(refined_text)
    else:
        token_output = tokenize_only(refined_text)
    # output_txt = ' '.join(token_output)

    return token_output  # ' '.join(token_output)


if __name__ == "__main__":
    print data_prep("What is employee classification and type policy".lower(),remove_stopwords=False)