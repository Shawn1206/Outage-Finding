import twint
import facebook_scraper

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


def reddit_scr():
    pass


def facebook_scr(group_id, credential):
    '''

    :param group_id: str
    :param credential:
    :return:
    '''
    data = facebook_scraper.get_posts(group=group_id,credentials=credential)
    pass


def forum_scr():
    pass
