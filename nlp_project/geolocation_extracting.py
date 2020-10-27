import en_core_web_sm
import spacy
import csv
from collections import defaultdict
import re
import geonamescache
import matplotlib.pyplot as plt
import credentials
import twitter
import json
from uszipcode import SearchEngine


def token_ex(clean_text):
    def markercleaner(string):
        pass

    def casehelper(string):
        new = string.split(' ')
        output = ''
        for i in range(len(new)):
            if new[i] and new[i] != ' ':
                new[i] = new[i][0].upper() + new[i][1:]
            output += new[i]
            if i != len(new) - 1:
                output += ' '
        return output

    tokens = clean_text.split(' ')
    clean_text = ''
    for token in tokens:
        new_token = ''.join(e for e in token if e.isalnum())
        clean_text += new_token + ' '
    nlp = en_core_web_sm.load()
    doc = nlp(clean_text)
    output = []
    for X in doc.ents:
        if X.label_ == 'GPE':
            output.append((X.text, X.label_))
    # if not output:
    words = clean_text.split(' ')
    for word in words:
        word = ''.join(e for e in word if e.isalnum())
        if word.isdigit() and len(word) == 5:
            search = SearchEngine(simple_zipcode=True)
            zipcode = search.by_zipcode(word)
            res = zipcode.to_dict()
            output.append((res['major_city'], 'GPE'))


    return output


# print(token_ex('1237270689087803392 2020-03-10 02:54:54 EDT <amyl_olsen> @Ask_Spectrum is there an outage in #NY?'))

def twitter_sp(name):
    def twitter_profile(user):
        consumer_key = credentials.consumer_key
        consumer_secret = credentials.consumer_secret
        access_token = credentials.access_token
        access_secret = credentials.access_secret
        api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token_key=access_token, \
                          access_token_secret=access_secret)
        # print(user)
        try:
            user_id = api.UsersLookup(screen_name=user)
            stat = user_id[0].location
        except:
            stat = ''
        # print(stat)
        return stat

    tmp = open(name, 'r')
    text = tmp.read()
    text = text.split('\n')[:-1]
    # print(len(set(text)))
    output = defaultdict(list)
    p1 = re.compile(r'[<](.*?)[>]')
    for tweet in text:
        # username = re.findall(p1, tweet)[0]
        geo_stat = ''
        # geo_stat = twitter_profile(username)
        time = tweet[20:44]
        msg = tweet[54::]
        if geo_stat:
            msg += geo_stat
        res = token_ex(msg)
        if res:
            output[time].append(res)
    with open('loca_' + name + '.json', 'w') as outfile:
        json.dump(output, outfile)


twitter_sp('Spectrum.txt')

# twitter_sp('New_data_AT&T.txt')
# twitter_sp('New_data_Verizon.txt')
# twitter_sp('New_data_Comcast.txt')
# twitter_sp('New_data_Cox.txt')


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


# reddit_sp('reddit_data4.csv')

def forum_sp(name):
    output = defaultdict(list)
    tmp = open(name, 'r')
    text = tmp.read()
    pages = text.split('Best Match')
    num = 0
    for page in pages:
        posts = page.split(' ' * 33)
        for post in posts:
            num += 1
            date = re.search(r"[0-1][0-9]-[0-2][0-9]-20[0-9][0-9]", post)
            time1 = re.search(r"[0-9][0-9]:[0-9][0-9]", post)
            time2 = re.search(r"[A-Z]M", post)
            if time2 and time1 and date:
                time_f = date.group() + ' ' + time1.group() + ' ' + time2.group()
                res = token_ex(post)
                if res:
                    output[time_f].append(token_ex(post))
    print(output)
    print(len(output))
    print(num)


# forum_sp('Xfinity_forum_data0.1.txt')

# def location_filter(dict0):
#     empty = []
#


#
#     gc = geonamescache.GeonamesCache()
#     county = {}
#     for coun in gc.get_us_counties():
#         county[coun['name']] = coun
#     for time in dict0.keys():
#         tmp = []
#         for post in dict0[time]:
#             tmp2 = []
#             for tuple in post:
#                 # if not tuple[0][0].isupper():
#                 #     tmp3 = casehelper(tuple[0])
#                 # else:
#                 #     tmp3 = tuple[0]
#                 tmp3 = casehelper(tuple[0])
#                 if tmp3 not in county and tmp3 not in gc.get_us_states_by_names() and \
#                         tmp3 not in gc.get_us_states() and gc.get_cities_by_name(tmp3) == []:
#                     print(tmp3)
#                     continue
#                 else:
#                     tmp2.append(tmp3)
#             tmp.append(tmp2)
#         if tmp[0]:
#             dict0[time] = tmp
#         else:
#             empty.append(time)
#     for key in empty:
#         dict0.pop(key)
#     return dict0


def name_to_number(name):
    pass

# gc = geonamescache.GeonamesCache()
# raw = gc.get_cities()
# raw2 = raw.copy()
# for i in raw:
#     if raw[i]['countrycode'] != 'US':
#         raw2.pop(i)
#
# print(len(raw2))

# print(len(dict0))
# print(location_filter(dict0))
