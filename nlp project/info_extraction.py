import en_core_web_sm
import spacy
from pprint import pprint

def text_cleaner(raw_text):
    clean_t = ''

    return clean_t

def token_ex(clean_text):
    nlp = en_core_web_sm.load()
    doc = nlp(clean_text)
    output = []
    for X in doc.ents:
        output.append((X.text, X.label_))
    return output





