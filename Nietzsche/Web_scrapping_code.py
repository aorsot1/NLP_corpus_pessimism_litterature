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

beyond = requests.get('https://www.gutenberg.org/cache/epub/4363/pg4363.txt')
zara = requests.get('https://www.gutenberg.org/files/1998/1998-0.txt')
morals = requests.get('https://www.gutenberg.org/files/52319/52319-0.txt')
ecce = requests.get('https://www.gutenberg.org/files/52190/52190-0.txt')
will = requests.get('https://www.gutenberg.org/files/52914/52914-0.txt')
anti = requests.get('https://www.gutenberg.org/cache/epub/19322/pg19322.txt')
tragedy = requests.get('https://www.gutenberg.org/files/51356/51356-0.txt')
human = requests.get('https://www.gutenberg.org/cache/epub/38145/pg38145.txt')
dawn = requests.get('https://www.gutenberg.org/files/39955/39955-0.txt')

texts = [beyond.text, zara.text, morals.text, ecce.text, will.text, 
         anti.text, tragedy.text, human.text, dawn.text]

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
 
books_dict = {'book': ['Beyond Good and Evil', 'Thus Spake Zarathustra', 
                       'The Genealogy of Morals', 'Ecce Homo', 'The Will to Power',
                       'The Antichrist', 'The Birth of Tragedy', 'Human, All Too Human',
                       'The Dawn of Day'],
              'text': texts}
df = pd.DataFrame.from_dict(data=books_dict, orient='columns')
df['text_clean'] = df['text'].astype(str)
df['text_clean'] = df['text_clean'].apply(_removeNonAscii)
df['text_clean'] = df['text_clean'].apply(func = make_lower_case)
df['text_clean'] = df['text_clean'].apply(func = remove_stop_words)
df['text_clean'] = df['text_clean'].apply(func=remove_punctuation)
df['text_clean'] = df['text_clean'].apply(func=remove_html)

df.to_csv('Nietzsche_works_corpus.csv', header=True)
