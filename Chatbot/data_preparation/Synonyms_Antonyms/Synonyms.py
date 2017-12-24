# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 11:38:04 2016

@author: Gayatri.k
"""

###### Synonyms ######
from nltk.corpus import wordnet as wn
from textblob import TextBlob

def synonyms(ask):    
    blob = TextBlob(ask)
    y=list()
    for word, pos in blob.tags:
        #print word, pos
        y.append(pos)
    
    indices = [j for j, i in enumerate(y) if i == 'VB'or i == 'VBZ' or i =='VBP' or i =='VBD' or i == 'VBN'
        or i == 'VBG' or i == 'RB' or i == 'RBR' or i == 'RBS'or i == 'RP'
        or i == 'VP ' or i == 'ADVP' or i == 'ADJP' or i=='JJ' or i == 'JJR' or i == 'JJS']
        
    z=list()
    for i in indices:
        z.append(blob.words[i])
        
    def synset(word):
        return wn.synsets(word)
        
    a=list()   
    for i in z:
        a.append(synset(i))
        
    if (len(a)>0):    
        b=list()
        for i in range(len(a)):
            if (len(a[i])>=3):
                for j in range(3):
                    b.append( a[i][j])
            
        c=list()
        for i in b:
            name, pos, sid = i.name().split('.')
            c.append(name)
        
        d=[c[x:x+3] for x in range(0, len(c),3)]
        
        for i,j in zip(z,range(len(d))):
            for k in range(3):  
                yield (ask.replace(i,d[j][k]))
 
