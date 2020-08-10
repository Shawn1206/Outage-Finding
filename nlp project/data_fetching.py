import twint
# import facebook_scraper
import psaw
import datetime as dt


def tweet_scr(name, key, since, out):
    """

    :param name: str "ATTHelp"
    :param key: str "Internet outage"
    :param since: str '2020-07-20 00:00:00'
    :param out: str
    :return: str
    """
    c = twint.Config()
    c.Username = name
    c.Lang = 'en'
    c.Search = key
    c.Since = since
    c.Output = '/Users/Linghao/Desktop/playground/test.txt'

    twint.run.Search(c)
    return 'Your data is in' + ' ' + out


def reddit_scr(keyword):
    '''

    :param keyword: search work
    :return: a list of objects, we can get the text of the posts by call the object's attribute selftext
    '''
    api = psaw.PushshiftAPI()
    start_time = int(dt.datetime(2020, 3, 1).timestamp())
    # output = list(api.search_submissions(after=start_time, q=keyword, limit=20))
    output = api.search_comments(after=start_time, q=keyword, limit=1)
    return output


def facebook_scr(group_id, credential):
    '''

    :param group_id: first click into the group and the id is the last part of its url
    :param credential:tuple of user and password to login before requesting the posts
    :return: generator object
    '''
#     data = facebook_scraper.get_posts(group=group_id, credentials=credential)
#     return data
    pass


def forum_scr():
    pass


# output = []
# result = reddit_scr('Internet Outage')
# for i in result:
#     output.append(i)
# print(output)

