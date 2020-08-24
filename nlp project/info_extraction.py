import en_core_web_sm
import spacy
import csv
from collections import defaultdict
import re
import geonamescache


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


# twitter_sp('comcastcares_outage_Xfinity.txt')

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


# forum_sp('forum_data0.1.txt')

def location_filter(dict0):
    empty = []
    def casehelper(string):
        new = string.split(' ')
        output = ''
        for i in range(len(new)):
            if new[i] != ' ':
                new[i] = new[i][0].upper() + new[i][1:]
            output += new[i]
            if i != len(new)-1:
                output += ' '
        return output

    gc = geonamescache.GeonamesCache()
    for time in dict0.keys():
        tmp = []
        for post in dict0[time]:
            tmp2 = []
            for tuple in post:
                if not tuple[0][0].isupper():
                    tmp3 = casehelper(tuple[0])
                else:
                    tmp3 = tuple[0]
                if tmp3 not in gc.get_us_states_by_names() and \
                        tmp3 not in gc.get_us_states() and gc.get_cities_by_name(tmp3) == []:
                    continue
                else:
                    tmp2.append(tmp3)
            tmp.append(tmp2)
        if tmp != [[]]:
            dict0[time] = tmp
        else:
            empty.append(time)
    for key in empty:
        dict0.pop(key)
    return dict0

# b = {'08-15-2020 04:58 PM': [[('Milpitas', 'GPE')]], '08-14-2020 11:45 AM': [[('Billing', 'GPE')]], '08-12-2020 12:50 PM': [[('Billing', 'GPE')]], '08-11-2020 11:40 AM': [[('Billing      ', 'GPE')]], '08-07-2020 05:42 PM': [[('Billing', 'GPE')]], '08-07-2020 01:26 PM': [[('Billing', 'GPE')]], '08-07-2020 09:23 AM': [[('Goose Creek', 'GPE'), ('Goose Creek', 'GPE'), ('South Carolina', 'GPE'), ('Charleston', 'GPE')]], '08-07-2020 12:55 AM': [[('Billing', 'GPE')]], '08-06-2020 06:16 PM': [[('Billing      ', 'GPE')]], '07-28-2020 06:01 PM': [[('United States', 'GPE')]], '07-25-2020 09:19 AM': [[('bajarrett1', 'GPE'), ('Billing', 'GPE')]], '07-24-2020 01:17 PM': [[('Billing', 'GPE')]], '07-23-2020 10:45 PM': [[('Billing', 'GPE')]], '07-20-2020 11:24 AM': [[('Detroit', 'GPE')]], '07-10-2020 11:59 AM': [[('Billing', 'GPE'), ('t.v.', 'GPE')]], '07-08-2020 09:17 AM': [[('DC', 'GPE')]], '06-16-2020 04:42 PM': [[('Channels', 'GPE')]], '06-15-2020 04:10 PM': [[('Xfinity', 'GPE')]], '06-14-2020 05:43 PM': [[('Sacramento', 'GPE')]], '06-11-2020 07:24 PM': [[('Channels', 'GPE')]], '06-11-2020 04:43 PM': [[('Catalina', 'GPE'), ('Cisco', 'GPE')]], '06-08-2020 07:31 CM': [[('CM600', 'GPE')]], '06-02-2020 09:45 PM': [[('Houston', 'GPE')]], '05-24-2020 03:08 AM': [[('Channels', 'GPE')]], '05-23-2020 08:09 PM': [[('bay_area', 'GPE'), ('Dropbox', 'GPE')]], '05-23-2020 08:00 PM': [[('North Port', 'GPE'), ('Fl', 'GPE'), ('Florida', 'GPE')]], '05-21-2020 08:08 PM': [[('Xfinity', 'GPE')]], '05-18-2020 07:56 PM': [[('Philadelphia', 'GPE')]], '05-18-2020 07:30 PM': [[('Chicago', 'GPE')]], '05-14-2020 06:12 PM': [[('Oakland', 'GPE')]], '05-12-2020 03:39 PM': [[('Tiltrelia', 'GPE')]], '05-09-2020 04:51 PM': [[('Louisiana', 'GPE')]], '05-07-2020 12:47 CM': [[('75Mbps', 'GPE')]], '05-06-2020 11:37 PM': [[('Kirkland', 'GPE'), ('WA', 'GPE')]], '05-06-2020 08:16 AM': [[('Billing', 'GPE')]], '05-03-2020 08:50 PM': [[('Houston', 'GPE')]], '05-02-2020 09:13 AM': [[('USA', 'GPE')]], '04-21-2020 10:42 PM': [[('Billing      ', 'GPE')]], '04-16-2020 05:07 PM': [[('US', 'GPE')]], '04-11-2020 12:41 PM': [[('India', 'GPE')]], '04-08-2020 04:57 PM': [[('Troubleshooting', 'GPE')]], '04-06-2020 04:21 PM': [[('Richmond Virginia', 'GPE')]], '04-04-2020 08:51 OM': [[('CA', 'GPE')]], '04-03-2020 06:53 PM': [[('dBmV', 'GPE'), ('Modem', 'GPE')]], '04-03-2020 05:29 PM': [[('San Francisco', 'GPE')]], '04-03-2020 12:37 PM': [[('CL17', 'GPE')]], '04-03-2020 01:28 AM': [[('Channels', 'GPE')]], '04-02-2020 08:28 AM': [[('palo alto', 'GPE')]], '04-01-2020 12:24 AM': [[('East Haven', 'GPE'), ('West Haven', 'GPE')]], '03-21-2020 05:49 PM': [[('San Mateo', 'GPE'), ('Foster City', 'GPE'), ('Burlingame', 'GPE'), ('Hillsborough', 'GPE'), ('Millbrae', 'GPE')]], '03-20-2020 03:45 PM': [[('Xfinity', 'GPE')]], '03-19-2020 07:50 PM': [[('line(s', 'GPE')]], '03-17-2020 02:48 PM': [[('HighCaliber', 'GPE'), ("Fort Lauderdale's", 'GPE')]], '03-14-2020 09:02 AM': [[('Channels', 'GPE')]], '03-09-2020 10:39 PM': [[('Gigabit', 'GPE'), ('nderstand', 'GPE')]], '02-22-2020 10:44 PM': [[('600s', 'GPE')]], '02-10-2020 10:51 AM': [[('2.4ghz', 'GPE')]], '01-27-2020 04:21 PM': [[('VM', 'GPE')]], '01-24-2020 07:32 PM': [[('RX', 'GPE')]], '01-24-2020 01:56 PM': [[('china', 'GPE')]], '01-21-2020 08:04 AM': [[('Channels', 'GPE'), ('Chicago', 'GPE')]], '01-20-2020 09:15 PM': [[('roku', 'GPE'), ('roku', 'GPE')]], '01-20-2020 04:50 PM': [[('Billing      ', 'GPE')]]}
# print(len(location_filter(a)))

def name_to_number():
    pass

