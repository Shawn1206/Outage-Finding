import csv
import datetime
import json
import random
import re
from collections import defaultdict

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import googlemaps
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from geonamescache import GeonamesCache
from haversine import haversine
from sklearn.cluster import DBSCAN

from constant import state_dict, state_list, capital_dic
from credentials import google_key


# lyon = (45.7597, 4.8422)
# paris = (48.8567, 2.3508)
#
# output = haversine(lyon, paris)
def G_helper(name):
    """
    this function is utilizing Google map API for getting coordinates of certain city
    :param name: city name, str
    :return: coordinates, tuple
    """
    gmaps = googlemaps.Client(key=google_key)

    geocode_result = gmaps.geocode(name)
    return geocode_result


def time_series(name_type, time_slot, gran):
    '''
    This is time_series generating function for getting statistics of raw data
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

    color = 'bygrm'
    n = 0
    tmp = [0] * 61
    tmp2 = []
    for dataset in name_type:
        out = counter(dataset)
        x, y = list(reversed(out.keys())), list(reversed(out.values()))
        tmp2 = x
        for i in range(61):
            tmp[i] += y[i]
        plt.plot(x, y, color=color[n], label=dataset[0].split('.')[0])
        # pickle.dump([x, y], open(dataset[0][:-4] + ' ' + time_slot[0] + ' for_tom.pkl', 'wb'))
        n += 1
    plt.title('Twitter Complaints about Outage 2019-2020')
    plt.plot(tmp2, tmp, color='k', label='total')
    plt.xlabel('Time Flow')
    plt.xticks(np.arange(0, 61, 7), rotation=0, fontsize=13)
    plt.ylabel('Number of tweets')
    plt.legend()
    plt.savefig('test')
    # plt.savefig(name_type[0][0][:-4] + ' ' + time_slot[0] + '.pdf', bbox_inches='tight')
    plt.show()


# ISP_lst = [('Verizon.txt', 't'), ('Spectrum.txt', 't'), ('Cox.txt', 't'), ('AT&T.txt', 't'), ('Comcast.txt', 't')]
# ISP_lst =[('Full_data_Spectrum.txt','t')]
# time_series(ISP_lst, ('2019-01-01', '2019-04-30'), 'month')
def geo_match2(location_names):
    def data_preprocess(data):
        data_formal = {}
        for i in data:
            time = datetime.datetime.strptime(i[:19], "%Y-%m-%dT%H:%M:%S")
            # the patter of timestamp could vary for different data source
            data_formal[str(time)] = [j[0] for j in data[i][0]]
        return data_formal

    location_names = data_preprocess(location_names)
    output = {}
    bad_items = []
    gc = GeonamesCache()
    state_dic_abbr = gc.get_us_states()
    new_data = {'DC': [38.895, -77.0366667], 'St. Paul': [44.9537, -93.0900]}
    with open("city_loca.json", 'r') as f2:
        for line in f2:
            datum = json.loads(line)
            if datum['CityNameAccented'] not in new_data:
                new_data[datum['CityNameAccented']] = [datum['Latitude'], datum['Longitude']]
    for i in location_names:
        s = len(output)
        for name in location_names[i]:
            # print(name)
            # print(new_data)
            if name in new_data:
                output[i] = new_data[name]
                break
            else:
                continue
        if i not in new_data:
            full_state_name = ''
            for name in location_names[i]:
                if name in state_dic_abbr:
                    full_state_name = state_dic_abbr[name]['name']
                else:
                    if name in capital_dic:
                        full_state_name = name
                if full_state_name:
                    tmp0 = capital_dic[full_state_name]
                    try:
                        output[i] = new_data[tmp0]
                        break
                    except:
                        continue
        e = len(output)
        if s==e:
            bad_items.append((i, location_names[i]))
    print(bad_items)
    # with open('coordinates_IstheServicedown_' + 'Verizon' + '.json', 'w') as outfile:
    #     json.dump(output, outfile)
    return output


f = open('loca_IstheServiceDown_spectrum.json')
data = json.load(f)
print(len(data))
print(len(geo_match2(data)))


def clustering(ISP_lst):
    global uni

    def time_location_clustering(isp_name, time_slot, time_gap, distance):
        '''
        This function returns clustered groups
        :param isp_name:
        :param time_slot:
        :param time_gap:
        :param distance:
        :return:
        '''

        def data_preprocess(data):
            data_formal = {}
            for i in data:
                time = datetime.datetime.strptime(i[:19], "%Y-%m-%d %H:%M:%S")
                data_formal[time] = [j[0] for j in data[i][0]]
            # print(data_formal)
            return data_formal

        def data_slice(data, start, end):
            output = {}
            for i in data:
                if start <= i <= end:
                    output[i] = data[i]
                else:
                    continue
            # print(output)
            return output

        # def geo_match2(location_names):
        #     output = {}
        #     gc = GeonamesCache()
        #     state_dic_abbr = gc.get_us_states()
        #     new_data = {'DC': [38.895, -77.0366667], 'St. Paul': [44.9537, -93.0900]}
        #     with open("city_loca.json", 'r') as f2:
        #         for line in f2:
        #             datum = json.loads(line)
        #             if datum['CityNameAccented'] not in new_data:
        #                 new_data[datum['CityNameAccented']] = [datum['Latitude'], datum['Longitude']]
        #     for i in location_names:
        #         for name in location_names[i]:
        #             if name in new_data:
        #                 output[i] = new_data[name]
        #                 break
        #             else:
        #                 continue
        #         if i not in new_data:
        #             full_state_name = ''
        #             for name in location_names[i]:
        #                 if name in state_dic_abbr:
        #                     full_state_name = state_dic_abbr[name]['name']
        #                 else:
        #                     if name in capital_dic:
        #                         full_state_name = name
        #                 if full_state_name:
        #                     tmp0 = capital_dic[full_state_name]
        #                     try:
        #                         output[i] = new_data[tmp0]
        #                         break
        #                     except:
        #                         continue
        #     # print(output)
        #     return output

        def clutering_time(data, time_gap):
            X = np.array(data)
            clustering = DBSCAN(eps=time_gap * 3600, min_samples=1).fit(X)
            labels = clustering.labels_
            pass

        def clustering_geo(data, distance):
            def center_g(member_list):
                x = sum([i[0] for i in member_list]) / len(member_list)
                y = sum([j[1] for j in member_list]) / len(member_list)
                c = (x, y)
                return c

            groups = []
            while data:
                curr = data.pop()
                if not groups:
                    groups.append([curr])
                else:
                    dist = []
                    for group in groups:
                        dist.append(haversine(curr, center_g(group)))
                    dist = np.array(dist)
                    if min(dist) <= distance:
                        groups[np.ndarray.argmin(dist)].append(curr)
                    else:
                        groups.append([curr])
            representatives = {}
            for group in groups:
                representatives[center_g(group)] = len(group)
            return representatives

        s, e = datetime.datetime.strptime(time_slot[0], "%Y-%m-%d"), datetime.datetime.strptime(
            time_slot[1], "%Y-%m-%d")
        f = open(isp_name)
        data = json.load(f)
        data_pre = data_preprocess(data)
        data_formal = geo_match2(data_pre)
        data_slice1 = data_slice(data_formal, s, e)
        tmp = data_slice1.values()
        groups = clustering_geo(list(tmp), distance)
        y, x = [i[0] + 0.2 * random.random() for i in groups.keys()], [i[1] + 0.2 * random.random() for i in
                                                                       groups.keys()]
        z = list(groups.values())
        return x, y, z

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(resolution='110m')
    ax.set_extent([-130, -60, 17, 50], ccrs.PlateCarree())
    ax.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle=':')
    ax.add_feature(cfeature.STATES.with_scale('50m'), linestyle=':')
    color = 'bygrm'
    for i, j in enumerate(ISP_lst):
        x, y, z = time_location_clustering(j[0], j[1], j[2], j[3])
        # uni += set(z)
        # print(len(x))
        # x = y = [30]
        # z = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 25, 28, 29]
        # z = [29]
        # for i in range(len(z)):
        #     plt.scatter(x, y, marker='o', c='k', s=z[i] * 30, label=str(z[i]) + ' tweets')
        # break
        for k in range(len(x)):
            if z[k] >= 3:
                plt.scatter([x[k]], [y[k]], s=z[k] * 30, marker='o', c=color[i], label=str(z[k]) + ' tweets')

    # plt.title(isp_name + ' from ' + time_slot[0] + ' to ' + time_slot[1])
    plt.title('Outage Reports for ISPs' + ' on' + ' March ' + ISP_lst[0][1][0].split('-')[-1] + 'th')
    plt.legend(loc=3)
    # plt.savefig(ISP_lst[0][1][1])
    plt.show()

# uni = []
# set(uni)
# pattern = '2020-03-'
#
# for i in range(2, 32):
#     time = (pattern + str(i - 1), pattern + str(i))
#     ISP_lst = [('loca_Verizon.json', time, 1, 500),
#                ('loca_Spectrum.json', time, 1, 500),
#                ('loca_Comcast.json', time, 1, 500),
#                ('loca_AT&T.json', time, 1, 500),
#                ('loca_Cox.json', time, 1, 500)]
#     clustering(ISP_lst)
#
# time = ('2020-03-31', '2020-04-01')
# clustering([('loca_Verizon.json', time, 1, 500),
#             ('loca_Spectrum.json', time, 1, 500),
#             ('loca_Comcast.json', time, 1, 500),
#             ('loca_AT&T.json', time, 1, 500),
#             ('loca_Cox.json', time, 1, 500)])
#
# pattern = '2020-04-'
# for i in range(2, 31):
#     time = (pattern + str(i - 1), pattern + str(i))
#     ISP_lst = [('loca_Verizon.json', time, 1, 500),
#                ('loca_Spectrum.json', time, 1, 500),
#                ('loca_Comcast.json', time, 1, 500),
#                ('loca_AT&T.json', time, 1, 500),
#                ('loca_Cox.json', time, 1, 500)]
#     clustering(ISP_lst)
# time = ('2020-04-30', '2020-05-01')
# clustering([('loca_Verizon.json', time, 1, 500),
#             ('loca_Spectrum.json', time, 1, 500),
#             ('loca_Comcast.json', time, 1, 500),
#             ('loca_AT&T.json', time, 1, 500),
#             ('loca_Cox.json', time, 1, 500)])
