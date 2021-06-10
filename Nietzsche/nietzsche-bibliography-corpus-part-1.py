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


# Beyond Good and Evil
beyond = requests.get('https://www.gutenberg.org/cache/epub/4363/pg4363.txt')
beg = beyond.text.find('PREFACE')
end = beyond.text.find('End of Project Gutenberg')
book1 = beyond.text[beg:end]


# In[3]:


# Thus Spoke Zarathustra
zara = requests.get('https://www.gutenberg.org/files/1998/1998-0.txt')
beg = zara.text.find('THUS SPAKE ZARATHUSTRA.')
end = zara.text.find('gloomy mountains.')
book2 = zara.text[beg:end]+'gloomy mountains.'


# In[4]:


# On the genealogy of morals
morals = requests.get('https://www.gutenberg.org/files/52319/52319-0.txt')
beg = morals.text.find('PREFACE.')
end = morals.text.find('does not betray us!')
book3 = morals.text[beg:end]+'does not betray us!'


# In[5]:


# Ecce Homo
ecce = requests.get('https://www.gutenberg.org/files/52190/52190-0.txt')
beg = ecce.text.find('PREFACE\r\n\r\n\r\n1')
end = ecce.text.find('End of Project Gutenberg')
book4 = ecce.text[beg:end]


# In[6]:


# Will to Power Part 1
will1 = requests.get('https://www.gutenberg.org/files/52914/52914-0.txt')
beg = will1.text.find('PREFACE.\r\n\r\n\r\n1')
end = will1.text.find('End of the Project Gutenberg')
book5a = will1.text[beg:end]


# In[7]:


# Will to Power Part 1
will2 = requests.get('https://www.gutenberg.org/files/52915/52915-0.txt')
beg = will2.text.find('THIRD BOOK.')
end = will2.text.find('End of the Project Gutenberg')
book5b = will2.text[beg:end]


# In[8]:


book5 = book5a + book5b


# In[9]:


# The Antichrist
anti = requests.get('https://www.gutenberg.org/cache/epub/19322/pg19322.txt')
beg = anti.text.find('PREFACE\r\n\r\n\r\nThis')
end = anti.text.find('End of the Project Gutenberg')
book6 = anti.text[beg:end]


# In[10]:


# The Birth od Tragedy
trag = requests.get('https://www.gutenberg.org/files/51356/51356-0.txt')
beg = trag.text.find('AN ATTEMPT AT SELF-CRITICISM.')
end = trag.text.find("TRANSLATOR\'S NOTE.\r\n\r\n\r\nWhile")
book7 = trag.text[beg:end]


# In[11]:


# Human, All Too Human
human = requests.get('https://www.gutenberg.org/cache/epub/38145/pg38145.txt')
beg = human.text.find('PREFACE.')
end = human.text.find("End of Project Gutenberg")
book8 = human.text[beg:end]


# In[12]:


# The Dawn of Day
dawn = requests.get('https://www.gutenberg.org/files/39955/39955-0.txt')
beg = dawn.text.find("AUTHORâ\x80\x99S PREFACE.")
end = dawn.text.find("FOOTNOTES")
book9 = dawn.text[beg:end]


# In[13]:


# Thoughts out of Season (Part I)
thought1 = requests.get('https://www.gutenberg.org/cache/epub/5652/pg5652.txt')
beg = thought1.text.find("DAVID STRAUSS,")
end = thought1.text.find("clarifier of the past.")
book10a = thought1.text[beg:end]+'clarifier of the past.'


# In[14]:


# Thoughts out of Season (Part II)
thought2 = requests.get('https://www.gutenberg.org/cache/epub/38226/pg38226.txt')
beg = thought2.text.find("THE USE AND ABUSE OF HISTORY.")
end = thought2.text.find("End of the Project Gutenberg")
book10b = thought2.text[beg:end]


# In[15]:


book10 = book10a +book10b


# In[16]:


# Homer and Classical Philology
homer = requests.get('https://www.gutenberg.org/cache/epub/18188/pg18188.txt')
beg = homer.text.find("HOMER AND CLASSICAL PHILOLOGY.")
end = homer.text.find("End of the Project Gutenberg EBook")
book11 = homer.text[beg:end]


# In[17]:


# We Philologists
wephilo = requests.get('https://www.gutenberg.org/cache/epub/18267/pg18267.txt')
beg = wephilo.text.find("I\r\n\r\n")
end = wephilo.text.find("FINIS.")
book12 = wephilo.text[beg:end]


# In[18]:


# The Case for Wagner
wagner = requests.get('https://www.gutenberg.org/files/25012/25012-0.txt')
beg = wagner.text.find("THE CASE OF WAGNER: A MUSICIAN")
end = wagner.text.find("\r\n\r\n\r\n\r\n\r\n\r\n\r\nFOOTNOTES")
book13 = wagner.text[beg:end]


# In[19]:


# On the future of our education
future = requests.get('https://www.gutenberg.org/files/28146/28146-0.txt')
beg = future.text.find("PREFACE.")
end = future.text.find("in common with me.--TR.")
book14 = future.text[beg:end]+"in common with me.--TR."


# In[20]:


# Early Greek Philosophy & Other Essays
greek = requests.get('https://www.gutenberg.org/files/51548/51548-0.txt')
beg = greek.text.find("THE GREEK STATE")
end = greek.text.find("THE END.")
book15 = greek.text[beg:end]+"THE END."


# In[21]:


# The Joyful Wisdom
joy = requests.get('https://www.gutenberg.org/files/52124/52124-0.txt')
beg = joy.text.find("PREFACE TO THE SECOND EDITION.")
end = joy.text.find("End of Project Gutenberg")
book16 = joy.text[beg:end]


# In[22]:


twilight = requests.get('https://www.gutenberg.org/files/52263/52263-0.txt')
beg = twilight.text.find("PREFACE\r\n\r\n\r\nTo maintain")
end = twilight.text.find("III., 29.")
book17 = twilight.text[beg:end]


# In[23]:


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


# In[24]:


titles = ['Beyond Good and Evil','Thus Spake Zarathustra: A Book for All and None', 
         'Thoughts out of Season','The Dawn of Day',
         'Homer and Classical Philology', 
         'We Philologists', 'The Antichrist',
         'The Case of Wagner, Nietzsche Contra Wagner, and Selected Aphorisms.',
         'On the Future of our Educational Institutions',
         'Human, All Too Human: A Book for Free Spirits',
         'The Birth of Tragedy; or, Hellenism and Pessimism',
         'Early Greek Philosophy & Other Essays', 'The Genealogy of Morals',
         'The Joyful Wisdom ("La Gaya Scienza")','Ecce Homo', 
         'The Twilight of the Idols; or, How to Philosophize with the Hammer',
         'The Will to Power: An Attempted Transvaluation of All Values']

publish_dates = [1886, 1885, 1909, 1881, 
                 1868, 1874, 1895, 1889,
                 1910, 1878, 1872, 1909,
                 1887, 1882, 1908, 1889,
                 1901]
texts = [book1,book2,book3,book4,book5,book6,
        book7,book8,book9,book10,book11,book12,
        book13,book14,book15,book16,book17]


# In[25]:


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


# In[26]:


df.to_csv('Nietzsche_works_corpus.csv', header=True)

