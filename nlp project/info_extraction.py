import en_core_web_sm
import spacy
import csv
from collections import defaultdict
import re


def preprocess(raw_text):
    clean_t = ''
    return clean_t


def token_ex(clean_text):
    nlp = en_core_web_sm.load()
    doc = nlp(clean_text)
    output = []
    for X in doc.ents:
        if X.label_ == 'GPE':
            output.append((X.text, X.label_))
    return output


def twitter_sp(name):
    tmp = open(name, 'r')
    text = tmp.read()
    text = text.split('\n')[:-1]
    output = defaultdict(list)
    for tweet in text:
        time = tweet[20:44]
        msg = tweet[54::]
        res = token_ex(msg)
        if res:
            output[time].append(res)
    print(output)


# twitter_sp('comcastcares.txt')

def reddit_sp(name):
    output = defaultdict(list)
    with open(name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            time = row[0]
            subre = row[1]
            txt = row[2] + ' ' + row[3]
            res_pre = token_ex(txt)
            if res_pre:
                output[time].append(res_pre)
    print(output)


# reddit_sp('reddit_data.csv')

def forum_sp(name):
    output = defaultdict(list)
    tmp = open(name, 'r')
    text = tmp.read()
    pages = text.split('Best Match')
    for page in pages:
        posts = page.split(' ' * 33)
        for post in posts:
            date = re.search(r"[0-1][0-9]-[0-2][0-9]-20[0-9][0-9]", post)
            time1 = re.search(r"[0-9][0-9]:[0-9][0-9]", post)
            time2 = re.search(r"[A-Z]M", post)
            if time2 and time1 and date:
                time_f = date.group()+' '+time1.group() +' '+time2.group()
                res = token_ex(post)
                if res:
                    output[time_f].append(token_ex(post))
    print(output)


# forum_sp('forum_data0.1.txt')
