import en_core_web_sm
import spacy
from pprint import pprint
import numpy as np


def preprocess(raw_text):
    clean_t = ''
    return clean_t


def token_ex(clean_text):
    nlp = en_core_web_sm.load()
    doc = nlp(clean_text)
    output = []
    for X in doc.ents:
        output.append((X.text, X.label_))
    return output

def twitter_sp(name):
    xfi = open(name, 'r')
    text = xfi.read()
    text = text.split('\n')[:-1]
    print(text)

twitter_sp('Xfinity.txt')
