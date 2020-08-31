import twint
import facebook_scraper
import psaw
import datetime as dt
import csv
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import sys
import time
import selenium


def tweet_scr(name, key, since,until, out):
    """

    :param name: str "ATTHelp"
    :param key: str "Internet outage"
    :param since: str '2020-07-20 00:00:00'
    :param out: str
    :return: str
    """
    c = twint.Config()
    # c.Search = "from:" + name
    # c.User_full = True
    c.Lang = 'en'
    c.Profile_full = True
    c.Search = key
    c.Since = since
    c.Until = until
    c.Output = out + name + '_' + key + ' ' + since + '.txt'

    twint.run.Search(c)
    return 'Your data is in' + ' ' + out


tweet_scr('Verizon', 'outage Verizon', '2019-01-01 00:00:00','2019-12-18 13:10:15', '/Users/xiaoan/Desktop/network/nlp project/data/')
# tweet_scr('CenturyLink', 'outage CenturyLink', '2019-01-01 00:00:00','2020-08-30 23:59:59', '/Users/xiaoan/Desktop/network/nlp project/data/')
tweet_scr('Cox', 'outage Cox', '2019-01-01 00:00:00','2019-11-01 03:55:04', '/Users/xiaoan/Desktop/network/nlp project/data/')

def reddit_scr(keyword):
    '''

    :param keyword: search work
    :return:
    '''
    api = psaw.PushshiftAPI()
    start_time = int(dt.datetime(2020, 1, 1).timestamp())
    output_raw = list(api.search_submissions(after=start_time, q=keyword, limit=100000000))
    # output = api.search_comments(after=start_time, q=keyword, limit=1)
    output = []
    curr = []
    for obj in output_raw:
        if obj.subreddit == 'Comcast_Xfinity':
            t = time.localtime(int(obj.created_utc))
            t2 = time.strftime("%Y-%m-%d %H:%M:%S", t)
            tf = dt.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
            curr.append(tf)
            curr.append(obj.subreddit)
            curr.append(obj.title)
            curr.append(obj.selftext)
            output.append(curr)
            curr = []

    file = open('reddit_data4.csv', 'a+', newline='')
    with file:
        write = csv.writer(file)
        write.writerows(output)
    return 'Done'


# result = reddit_scr('outage')


def facebook_scr(group_id, credential):
    '''

    :param group_id: first click into the group and the id is the last part of its url
    :param credential:tuple of user and password to login before requesting the posts
    :return: generator object
    '''
    data = facebook_scraper.get_posts(group=group_id, credentials=credential)
    return data


# data = facebook_scr('434568226894938', ('121472974@qq.com', 'Peter0316'))
# for i in data:
#     print(i)
#     break
# output = []
# for i in result:
#     output.append(i)
# print(output)

def forum_scr(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request, timeout=20)
    html = response.read()

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
    file.write(text)
    # file.write('\n')
    return text

# num = 1
# while num < 3:
#     num = str(num)
#     forum_scr('https://forums.xfinity.com/t5/forums/searchpage/tab/message?q=outage&advanced=true&page='+ num +'&sort_by=-topicPostDate&collapse_discussion=true&search_type=thread&search_page_size=10')
#     num = int(num)
#     num += 1
