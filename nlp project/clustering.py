import json
from haversine import haversine
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
# import cartopy
from collections import defaultdict
import csv
import re
import time
import datetime
import pickle


# lyon = (45.7597, 4.8422)
# paris = (48.8567, 2.3508)
#
# output = haversine(lyon, paris)


def geomatch(data):
    output = []
    new_data = {}
    with open("city_loca.json", 'r') as f:
        for line in f:
            datum = json.loads(line)
            if 'Population' in datum:
                new_data[datum['CityNameAccented']] = [datum['Latitude'], datum['Longitude']]
    for i in data.values():
        # print(i)
        for event in i:
            # print(event)
            if event[0] in new_data:
                # print(event[0])
                coord = new_data[event[0]]  # can be improved
                output.append(coord)
                break
    return output


def clustering_distance(distance, data, min_p):
    new_data = geomatch(data)
    X = np.array(new_data)
    clustering = DBSCAN(eps=distance, min_samples=min_p, metric=haversine).fit(X)
    labels = clustering.labels_
    core_samples_mask = np.zeros_like(clustering.labels_, dtype=bool)
    core_samples_mask[clustering.core_sample_indices_] = True
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    # n_noise_ = list(labels).count(-1)
    unique_labels = set(labels)
    colors = [plt.cm.get_cmap('Spectral')(each) for each in np.linspace(0, 1, len(unique_labels))]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.xlabel('latitude')
    plt.ylabel('longitude')
    plt.show()





def clustering_time(name_type, time_slot, gran):
    '''

    :param name_type: [('Comcast.txt','t')]
    :param time_slot: ('2020-08-01','2020-09-01')
    :param gran: 'week','day','month'
    :return:
    '''
    s, e = datetime.datetime.strptime(time_slot[0], "%Y-%m-%d"), datetime.datetime.strptime(
        time_slot[1], "%Y-%m-%d")

    def counter(name_type):
        check = []
        time_flow = defaultdict(int)
        name = name_type[0]
        type = name_type[1]
        if type == 'r':
            with open(name, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    time = row[0][:7]
                    date_time = datetime.datetime.strptime(time, "%Y-%m-%d")
                    if s <= date_time <= e:
                        tmp = granset(time, gran)
                        time_flow[tmp] += 1
        else:
            tmp = open(name, 'r')
            text = tmp.read()
            if type == 't':
                text = text.split('\n')[:-1]
                for tweet in text:
                    id = tweet[:19]
                    if id in check:
                        continue
                    else:
                        check.append(id)
                    time = tweet[20:30]
                    try:
                        date_time = datetime.datetime.strptime(time, "%Y-%m-%d")
                    except:
                        continue
                    if s <= date_time <= e:
                        tmp = granset(time, gran)
                        time_flow[tmp] += 1
            elif type == 'f':
                pages = text.split('Best Match')
                for page in pages:
                    posts = page.split(' ' * 33)
                    for post in posts:
                        date = re.search(r"[0-1][0-9]-[0-2][0-9]-20[0-9][0-9]", post)
                        if date:
                            time = date.group()[:2]
                            date_time = datetime.datetime.strptime(time, "%m-%d-%Y")
                            time = str(date_time)[:10]
                            if s <= date_time <= e:
                                tmp = granset(time, gran)
                                time_flow[tmp] += 1
        return time_flow

    def granset(time, gran):
        if gran == 'month':
            return time[:7]
        elif gran == 'week':
            pass
        else:
            return time

    color = 'bgrcmyk'
    n = 0
    for dataset in name_type:
        out = counter(dataset)
        x, y = list(reversed(out.keys())), list(reversed(out.values()))
        plt.plot(x, y, color=color[n], label=dataset[0])
        pickle.dump([x, y], open(dataset[0][:-4] + ' ' + time_slot[0] + ' for_tom.pkl', 'wb'))
        n += 1
    plt.title('Twitter Complaints about Outage 2019-2020')
    plt.xlabel('Time Flow')
    plt.xticks(rotation=90)
    plt.ylabel('Number of tweets')
    plt.legend()
    plt.savefig(name_type[0][0][:-4] + ' ' + time_slot[0] + '.pdf', bbox_inches='tight')


lst = [('AT&T_outage AT&T.txt', 't'), ('Spectrum_outage Spectrum.txt', 't'), ('Cox.txt', 't'),
       ('Comcast_outage Xfinity.txt', 't'), ('Verizon_outage Verizon.txt', 't')]

clustering_time(lst, ('2019-01-01', '2020-08-30'), 'month')
# clustering_time(lst, ('2020-04-01', '2020-04-30'), 'day')
