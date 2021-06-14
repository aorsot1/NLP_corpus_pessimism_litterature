#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd

import math
import os
import re
import string
import random
import urllib3.request
import zipfile
import requests

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore")


# In[2]:


# The Art of Literature
lit = requests.get('https://www.gutenberg.org/cache/epub/10714/pg10714.txt')
beg = lit.text.find('ON AUTHORSHIP.')
end = lit.text.find('End of Project Gutenberg')
book1 = lit.text[beg:end]


# In[3]:


# THE ART OF CONTROVERSY
cont = requests.get('https://www.gutenberg.org/cache/epub/10731/pg10731.txt')
beg = cont.text.find('THE ART OF CONTROVERSY.')
end = cont.text.find('comprehensive understanding of it.')
book2 = cont.text[beg:end]+'comprehensive understanding of it.'


# In[4]:


# Counsels and Maxims
maxs = requests.get('https://www.gutenberg.org/cache/epub/10715/pg10715.txt')
beg = maxs.text.find('INTRODUCTION.')
end = maxs.text.find('End of Project Gutenberg')
book3 = maxs.text[beg:end]


# In[5]:


# Studies in Pessimism
pess = requests.get('https://www.gutenberg.org/cache/epub/10732/pg10732.txt')
beg = pess.text.find('ON THE SUFFERINGS OF THE WORLD.')
end = pess.text.find('***END OF THE PROJECT GUTENBERG EBOOK')
book4 = pess.text[beg:end]


# In[6]:


# ON HUMAN NATURE
human = requests.get('https://www.gutenberg.org/cache/epub/10739/pg10739.txt')
beg = human.text.find('HUMAN NATURE.\r\n\r\n\r\nTruths')
end = human.text.find('End of the Project Gutenberg EBook')
book5 = human.text[beg:end]


# In[7]:


# ON The Wisdom of Life
wisdom = requests.get('https://www.gutenberg.org/cache/epub/10741/pg10741.txt')
beg = wisdom.text.find('INTRODUCTION.')
end = wisdom.text.find('End of the Project Gutenberg EBook')
book6 = wisdom.text[beg:end]


# In[8]:


# Religion, A Dialogue
wisdom = requests.get('https://www.gutenberg.org/cache/epub/10833/pg10833.txt')
beg = wisdom.text.find('RELIGION.\r\n\r\nA DIALOGUE.\r\n\r\n\r\n_Demopheles_. ')
end = wisdom.text.find('***END OF THE PROJECT GUTENBERG EBOOK')
book7 = wisdom.text[beg:end]


# In[9]:


# Essays (Notes to add)
esy = requests.get('https://www.gutenberg.org/files/11945/11945-0.txt')
beg = esy.text.find('ESSAYS OF SCHOPENHAUER.')
end = esy.text.find('End of Project Gutenberg')
book8 = esy.text[beg:end]


# In[10]:


# World as Will 1
will1 = requests.get('https://www.gutenberg.org/files/38427/38427-0.txt')
beg = will1.text.find('PREFACE TO THE FIRST EDITION.')
end = will1.text.find('***END OF THE PROJECT GUTENBERG EBOOK')
book9 = will1.text[beg:end]


# In[11]:


# World as Will 2
will2 = requests.get('https://www.gutenberg.org/files/40097/40097-0.txt')
beg = will2.text.find('APPENDIX: CRITICISM OF THE KANTIAN PHILOSOPHY.')
end = will2.text.find('***END OF THE PROJECT GUTENBERG EBOOK')
book10 = will2.text[beg:end]


# In[12]:


# World as Will 3
will3 = requests.get('https://www.gutenberg.org/files/40868/40868-0.txt')
beg = will3.text.find('SUPPLEMENTS TO THE SECOND BOOK.')
end = will3.text.find('***END OF THE PROJECT GUTENBERG EBOOK')
book11 = will3.text[beg:end]


# In[13]:


# The Basis of Morality
mor = requests.get('https://www.gutenberg.org/files/44929/44929-0.txt')
beg = mor.text.find('The question advanced by the Royal Society,')
end = mor.text.find('End of Project Gutenberg')
book12 = mor.text[beg:end]


# In[14]:


# On the Fourfold Root
four = requests.get('https://www.gutenberg.org/files/50966/50966-0.txt')
beg = four.text.find('The divine Plato and the marvellous Kant')
end = four.text.find('End of the Project Gutenberg EBook')
book13 = four.text[beg:end]


# In[15]:


#Utitlity functions for removing ASCII characters, converting lower case, removing stop words, html and punctuation from description
def _removeNonAscii(s):
    return "".join(i for i in s if  ord(i)<128)

def make_lower_case(text):
    return text.lower()

def remove_stop_words(text):
    text = text.split()
    stops = set(stopwords.words("english"))
    text = [w for w in text if not w in stops]
    text = " ".join(text)
    return text

def remove_html(text):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)

def remove_punctuation(text):
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    text = " ".join(text)
    return text


# In[16]:


titles = ['The Art of Literature', 'The Art of Controversy',
          'Counsels and Maxims', 'Studies in Pessimism',
          'On Human Nature', 'On the Wisdom of Life', 
          'Religion, A dialogue', 'Essays',
          'The World As Will And Idea (Vol. 1 of 3)',
          'The World As Will And Idea (Vol. 2 of 3)',
          'The World As Will And Idea (Vol. 3 of 3)',
          'The Basis of Morality', 
          'On the Fourfold Root of the Principle of Sufficient Reason and On the Will in Nature']

publish_dates = [1890, 1831, 1851, 
                 1851, 1851, 1851, 
                 1851, 1851, 1819, 
                 1844, 1844, 1840, 
                 1813]

texts = [book1,book2,book3,book4,
         book5,book6,book7,book8,
         book9,book10,book11,book12, 
         book13]


# In[17]:


books_dict = {'book_title': titles,
              'publishing_date': publish_dates,
              'text': texts}
df = pd.DataFrame.from_dict(data=books_dict, orient='columns')
df['text_clean'] = df['text'].astype(str)
df['text_clean'] = df['text_clean'].apply(_removeNonAscii)
df['text_clean'] = df['text_clean'].apply(func = make_lower_case)
df['text_clean'] = df['text_clean'].apply(func = remove_stop_words)
df['text_clean'] = df['text_clean'].apply(func=remove_punctuation)
df['text_clean'] = df['text_clean'].apply(func=remove_html)


# In[18]:


df.to_csv('Schopenhauer_works_corpus.csv', header=True)

