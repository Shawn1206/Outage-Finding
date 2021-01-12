# this script is used for extracting location names from the raw scrapped dataset
import en_core_web_sm
import csv
from collections import defaultdict
import re
import credentials
import twitter
import json
from uszipcode import SearchEngine


def token_ex(clean_text):
    """
    This is the core function of this file, it takes text as input and return with the latent location names
    :param clean_text: str
    :return: list of wanted tuples, each tuple is (str, 'GPE')
    """
    def casehelper(string):
        """
        This is a helper function to compulsively capitalize every initial letter among the words of the input string.
        To make it easier for the NLP algorithm to recognize location names
        :param string: str
        :return: str
        """
        new = string.split(' ')
        output = ''
        for i in range(len(new)):
            if new[i] and new[i] != ' ':
                new[i] = new[i][0].upper() + new[i][1:]
            output += new[i]
            if i != len(new) - 1:
                output += ' '
        return output

    # clean the input text, and only keeps tokens which only consist of numbers and alphabets
    tokens = clean_text.split(' ')
    clean_text = ''
    for token in tokens:
        new_token = ''.join(e for e in token if e.isalnum())
        clean_text += new_token + ' '

    # Using NLP API
    nlp = en_core_web_sm.load()
    doc = nlp(clean_text)
    output = []
    for X in doc.ents:
        # print((X.text, X.label_))
        if X.label_ == 'GPE':
            output.append((X.text, X.label_))

    words = clean_text.split(' ')
    for word in words:
        word = ''.join(e for e in word if e.isalnum())
        # this is how we find zipcodes and convert them to actual locations then add them in the output
        if word.isdigit() and len(word) == 5:
            search = SearchEngine(simple_zipcode=True)
            zipcode = search.by_zipcode(word)
            res = zipcode.to_dict()
            output.append((res['major_city'], 'GPE'))

    return output


# print(token_ex("My Spectrum has been on the blink all morning and now it is totally out. Anyone else in 76114 area having same problem"))

def twitter_sp(name):
    """
    This function is dedicated to extract location names from Twitter data
    :param name: str, filename
    :return: None
    """
    def twitter_profile(user):
        """
        This function fetch the the Twitter user's profiles for the location in them
        :param user: str, user name
        :return: str, user location
        """
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
    p1 = re.compile(r'[<](.*?)[>]')  # pattern for getting the user name in the text
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


# twitter_sp('New_data_Re_AT&T.txt')

# twitter_sp('New_data_AT&T.txt')
# twitter_sp('New_data_Verizon.txt')
# twitter_sp('New_data_Comcast.txt')
# twitter_sp('New_data_Cox.txt')

def disqus(name_list):
    """
    This function is dedicated to extract location names from disqus data
    :param name_list: list, list of filenames
    :return: None
    """
    output = defaultdict(list)
    count = 0
    for name in name_list:
        with open(name, newline='') as tsvfile:  # the typical way of reading a tsv/csv file
            reader = csv.reader(tsvfile, delimiter='\t')
            for row in reader:
                count += 1
                # locate the data column you want
                time = row[1]
                txt = row[-1]
                if token_ex(txt):  # if any location name is found by our token_ex() function append it
                    output[time].append(token_ex(txt))
    with open('loca_istheServiceDown_' + name_list[0][41:-4] + '.json', 'w') as outfile:
        json.dump(output, outfile)
    # print(count)

#
# disqus(['./istheservicedown_Data/istheservicedown_cox.tsv'])
# disqus(['./istheservicedown_Data/istheservicedown_comcast.tsv'])
# disqus(['./istheservicedown_Data/istheservicedown_spectrum.tsv'])
# disqus(['./istheservicedown_Data/istheservicedown_verizon.tsv'])

def reddit_sp(name):
    """
    This function is dedicated to extract location names from reddit data
    :param name:str, filename
    :return: dict, {time: location}
    """
    output = defaultdict(list)
    with open(name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')  # the typical way of reading a tsv/csv file
        for row in reader:
            # locate the data column you want
            time = row[0]
            subre = row[1]
            txt = row[2] + ' ' + row[3]
            res_pre = token_ex(txt)
            if res_pre:
                output[time].append(res_pre)
    print(output)


# reddit_sp('reddit_data4.csv')

def forum_sp(name):
    """
    This function is dedicated to extract location names from Xfinity's official forum data
    :param name: str, filename
    :return: dict, {time: location}
    """
    output = defaultdict(list)
    tmp = open(name, 'r')
    text = tmp.read()
    # the following method is based on what I observed from the raw text data
    # So this might not very helpful on other forum with different webpage setting
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
                time_f = date.group() + ' ' + time1.group() + ' ' + time2.group()  # combine all time elements to
                # make a full timestamp
                res = token_ex(post)
                if res:
                    output[time_f].append(token_ex(post))
    print(output)
    print(len(output))
    print(num)


# forum_sp('Xfinity_forum_data0.1.txt')

def mailing_list(archive_list):
    """
    This function is dedicated to extract location names from mailing list archive
    :param archive_list: list, names of archive
    :return: dict, {time: location}
    """
    output = defaultdict(list)
    for archive in archive_list:
        tmp = open(archive, 'r')
        text = tmp.read()
        posts = text.split('\nFrom ')
        for post in posts:
            if 'CenturyLink' in posts[1]:
                pass


    pass
# mailing_list(['./Outage_Archives/2020-November.txt'])
