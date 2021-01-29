# this script is used for fetching data and form a file from different social media
import twint
import psaw
import datetime as dt
import csv
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import time
import credentials
import pandas as pd


def tweet_scr(key, since, until, out):
    """
    this function is dedicated to scrap Twitter data using Twint
    :param key: str, keyword using for searching
    :param since: str, start time of wanted data
    :param until: str, end time of wanted data
    :param out: str, output directory
    :return: str
    """

    # this function is to add a column of the used keyword to the raw output
    # And you can change the input or even tweak the code to fit your need of adding other columns to your data
    def attr_adding(fileName, keyword, new_column_name):
        data = pd.read_csv(fileName)
        data_tmp = [keyword] * len(data)
        data[new_column_name] = data_tmp
        data.to_csv(fileName)

    c = twint.Config()
    c.Search = "from:" + key  # when searching within certain account use "from:" + id
    # c.User_full = True
    c.Lang = 'en'
    c.Profile_full = True
    # c.Search = key  # normal searching using key as keyword
    c.Since = since
    c.Until = until
    c.Store_csv = True  # set output format to be csv
    file_name = out + key + ' ' + since + '.csv'
    c.Output = file_name
    # c.Output = "none"
    twint.run.Search(c)
    attr_adding(file_name, key, 'Keyword_set')
    return 'Your data is in' + ' ' + out







def reddit_scr(keyword):
    '''
    this function is dedicated to scrap reddit data using psaw
    :param keyword: str, keyword used for searching
    :return: str
    '''
    # use psaw's API
    api = psaw.PushshiftAPI()
    start_time = int(dt.datetime(2020, 1, 1).timestamp())
    output_raw = list(api.search_submissions(after=start_time, q=keyword, limit=100000000))
    # output = api.search_comments(after=start_time, q=keyword, limit=1)
    output = []
    curr = []  # this list is used for holding an entry before putting it into the final csv file
    for obj in output_raw:
        if obj.subreddit == 'Comcast_Xfinity':
            # convert the timestamp to a more convenient format
            t = time.localtime(int(obj.created_utc))
            t2 = time.strftime("%Y-%m-%d %H:%M:%S", t)
            tf = dt.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
            # combine the attributes to form an entry
            curr.append(tf)
            curr.append(obj.subreddit)
            curr.append(obj.title)
            curr.append(obj.selftext)
            # append the entry into output
            output.append(curr)
            curr = []
    # form the csv file
    file = open('reddit_data4.csv', 'a+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(output)
    return 'Done'





def forum_scr(url):
    """
    this function is used for scrapping data from Xfinity's official forum
    https://forums.xfinity.com/t5/forums/searchpage/tab/message?q=outage&sort_by=-topicPostDate&collapse_discussion=true
    :param url: str, input the url of the forum
    :return: None
    """
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request, timeout=20)
    html = response.read()  # fetch html file

    def tagVisible(element):
        '''
        Input: an element which is a child of the whole html document object -> str
        Output: if it contain plain text that we want -> boolean
        '''
        unwantedElements = ['style', 'script', 'head', 'title', 'meta', '[document]']
        if element.parent.name in unwantedElements:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def textFromHtml(body):
        '''
        Input: a html document that may contain js scripts, css styles and other stuff -> str
        Output: a clean text (<20000 characters) that only contains plain text
        '''
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(tagVisible, texts)
        cleanText = u" ".join(t.strip() for t in visible_texts)
        return cleanText

    text = textFromHtml(html)
    file = open('forum_data.txt', 'a')
    file.write(text)  # write down the text we found
    # file.write('\n')
    return



if __name__ == "__main__":
    # the follow code manipulate url to get different pages of the forum
    num = 1
    while num < 3:
        num = str(num)
        forum_scr('https://forums.xfinity.com/t5/forums/searchpage/tab/message?q=outage&advanced=true&page='+ num +'&sort_by=-topicPostDate&collapse_discussion=true&search_type=thread&search_page_size=10')
        num = int(num)
        num += 1

    # the follow line scrapes reddit data searching 'outage' as keywords
    result = reddit_scr('outage')
    
    # the follow code scrapes Twitter data using different keyword combo
    a = ['no', 'knocked', 'down', 'out']
    b = ['internet', 'service', 'network']
    isp = ['Comcast', 'Xfinity', 'Verizon', 'Fios', 'Spectrum', 'TWC', 'Cox', 'AT&T', 'DIRECTV']

    for i in a:
        for j in b:
            for k in isp:
                key = i + ' ' + j + ' ' + k
                # print(key)
                tweet_scr(key, '2019-01-01 00:00:00', '2020-08-31 23:59:59','/Users/xiaoan/Desktop/network/nlp_project/data/')
    
