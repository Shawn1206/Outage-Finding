# this script is used for clustering and time series analysis, and then generating plots
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
from geonamescache import GeonamesCache
from haversine import haversine
from sklearn.cluster import DBSCAN

from constant import state_dict, state_list, capital_dic, directions
from credentials import google_key


def G_helper(name):  # this function is temporarily not used
    """
    this function is utilizing Google map API for getting coordinates of certain city
    :param name: city name, str
    :return: coordinates, tuple
    """
    gmaps = googlemaps.Client(key=google_key)  # the key is imported from credentials.py

    geocode_result = gmaps.geocode(name)
    return geocode_result


def time_series(name_type, time_slot, gran):
    '''
    This is time_series generating function for getting statistics of raw data
    :param name_type: [('Comcast.txt','t_csv')], list of tuples, for each tuple it contains the file name and data source
    't' = Twitter_txt, 't_csv' = Twitter_csv, 'r' = Reddit, 'f' = forum
    :param time_slot: ('2020-08-01','2020-09-01')
    :param gran: 'week','day','month'
    :return:
    '''
    s, e = datetime.datetime.strptime(time_slot[0], "%Y-%m-%d"), datetime.datetime.strptime(
        time_slot[1], "%Y-%m-%d")  # set the start date and end date first

    def counter(name_type):
        """
        this function is for counting the number of raw data entries according to their date
        :param name_type: 't' = Twitter_txt, 't_csv' = Twitter_csv, 'r' = Reddit, 'f' = forum
        :return: dict, time flow
        """
        check = []
        time_flow = defaultdict(int)
        name = name_type[0]
        type = name_type[1]
        if type == 'r':
            with open(name, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    time = row[0][:7]
                    date_time = datetime.datetime.strptime(time, "%Y-%m-%d")  # change datatype of date
                    if s <= date_time <= e:
                        tmp = granset(time, gran)  # set the time granularity
                        time_flow[tmp] += 1
        if type == 't_csv':
            with open(name, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    time = row[3][:7]
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
                    if id in check:  # check if this entry has been examined
                        continue
                    else:
                        check.append(id)
                    time = tweet[20:30]  # locate the time
                    try:
                        date_time = datetime.datetime.strptime(time, "%Y-%m-%d")
                    except:
                        continue
                    if s <= date_time <= e:
                        tmp = granset(time, gran)  # set the granularity
                        time_flow[tmp] += 1
            elif type == 'f':
                pages = text.split('Best Match')
                for page in pages:
                    posts = page.split(' ' * 33)
                    for post in posts:
                        date = re.search(r"[0-1][0-9]-[0-2][0-9]-20[0-9][0-9]", post)  # locate the date
                        if date:
                            time = date.group()[:2]
                            date_time = datetime.datetime.strptime(time, "%m-%d-%Y")
                            time = str(date_time)[:10]
                            if s <= date_time <= e:
                                tmp = granset(time, gran)
                                time_flow[tmp] += 1
        return time_flow

    def granset(time, gran):
        """
        set the granularity
        :param time: str, whole timestamp
        :param gran: str, granularity, 'month' or 'day'
        :return: str, sliced timestamp
        """
        if gran == 'month':
            return time[:7]
        elif gran == 'week':
            pass
        else:
            return time

    # make the time series plot
    color = 'bygrm'  # hardcode the colors that would be used
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




def clustering(ISP_lst):
    """
    this function is for clustering data extracted from raw data via different methods and make plots
    :param ISP_lst: list of tuples
    :return: None
    """
    global uni

    def time_location_clustering(isp_name, time_slot, time_gap, distance):
        '''
        This function returns clustered groups
        sample input: ('loca_Verizon.json', ('2020-03-31', '2020-04-01'), 1, 500)
        :param isp_name: str, file name of extracted data
        :param time_slot: tuple, start and end date
        :param time_gap: int, the length of gap which determine the clustering
        :param distance: int, the distance which determine the clustering
        :return: None
        '''

        def data_preprocess(data):
            """
            this function is for unify the format of the timestamp
            :param data: dict
            :return: dict
            """
            data_formal = {}
            for i in data:
                time = datetime.datetime.strptime(i[:19], "%Y-%m-%d %H:%M:%S")
                data_formal[time] = [j[0] for j in data[i][0]]
            # print(data_formal)
            return data_formal

        def data_slice(data, start, end):
            """
            this function is for slice the data at will
            :param data: dict
            :param start: datetime, start time
            :param end: datetime, end time
            :return:
            """
            output = {}
            for i in data:
                if start <= i <= end:
                    output[i] = data[i]
                else:
                    continue
            # print(output)
            return output

        def geo_match2(location_names):
            """
            This function match US city names with corresponding coordinates, basically the same as
            coordinates_converting.py, check it for comments and description
            :param location_names: str, content of input file
            :return: str
            """
            output = {}
            gc = GeonamesCache()
            state_dic_abbr = gc.get_us_states()
            new_data = {'DC': [38.895, -77.0366667], 'St. Paul': [44.9537, -93.0900]}
            with open("city_loca.json", 'r') as f2:
                for line in f2:
                    datum = json.loads(line)
                    if datum['CityNameAccented'] not in new_data:
                        new_data[datum['CityNameAccented']] = [datum['Latitude'], datum['Longitude']]
            for i in location_names:
                for name in location_names[i]:
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
            # print(output)
            return output

        def clutering_time(data, time_gap):
            """
            this is an unfinished function dedicated to clustering data according to time
            :param data:
            :param time_gap:
            :return:
            """
            X = np.array(data)
            clustering = DBSCAN(eps=time_gap * 3600, min_samples=1).fit(X)
            labels = clustering.labels_
            pass

        def clustering_geo(data, distance):
            """
            this function is for clustering data according to their geolocation
            :param data: dict
            :param distance: int
            :return: dict, clustered groups
            """
            def center_g(member_list):
                """
                calculate the center(average) coordinate of a group of coordinates
                :param member_list:
                :return:
                """
                x = sum([i[0] for i in member_list]) / len(member_list)
                y = sum([j[1] for j in member_list]) / len(member_list)
                c = (x, y)
                return c
            # the following lines divide dots into groups
            groups = []
            while data:
                curr = data.pop()
                if not groups:
                    groups.append([curr])  # initiate the algorithm with adding the first dot as the first group
                else:
                    dist = []
                    for group in groups:
                        dist.append(haversine(curr, center_g(group)))  # calculate the distance between the new dot and the current groups
                    dist = np.array(dist)
                    if min(dist) <= distance:  # if the requirement is satisfied, find the nearest group and add the dot in
                        groups[np.ndarray.argmin(dist)].append(curr)
                    else:
                        groups.append([curr])  # if not, it would form a new group itself
            representatives = {}
            for group in groups:
                representatives[center_g(group)] = len(group)
            return representatives

        s, e = datetime.datetime.strptime(time_slot[0], "%Y-%m-%d"), datetime.datetime.strptime(
            time_slot[1], "%Y-%m-%d")
        f = open(isp_name)
        data = json.load(f)
        # preprocess the data
        data_pre = data_preprocess(data)
        data_formal = geo_match2(data_pre)
        data_slice1 = data_slice(data_formal, s, e)
        tmp = data_slice1.values()
        groups = clustering_geo(list(tmp), distance)
        y, x = [i[0] + 0.2 * random.random() for i in groups.keys()], [i[1] + 0.2 * random.random() for i in
                                                                       groups.keys()]
        # add some random noise to make the points more recognizable
        z = list(groups.values())
        return x, y, z
    # set the plate-carree map for projecting dots on it
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines(resolution='110m')
    ax.set_extent([-130, -60, 17, 50], ccrs.PlateCarree())
    ax.add_feature(cfeature.BORDERS.with_scale('50m'), linestyle=':')
    ax.add_feature(cfeature.STATES.with_scale('50m'), linestyle=':')
    # drawing dots on the map
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
    plt.savefig(ISP_lst[0][1][1])
    plt.show()



if __name__ == "__main__":
    # sample usage of generating a time series plot from the start of Jan 2019 to the end of April 2019
    ISP_lst = [('Verizon.txt', 't'), ('Spectrum.txt', 't'), ('Cox.txt', 't'), ('AT&T.txt', 't'), ('Comcast.txt', 't')]
    time_series(ISP_lst, ('2019-01-01', '2019-04-30'), 'month')
    
    # sample usage of generating a plot after clustering all five ISPs' data on March 2020
    uni = []
    set(uni)
    pattern = '2020-03-'

    for i in range(2, 32):
        time = (pattern + str(i - 1), pattern + str(i))
        ISP_lst = [('loca_Verizon.json', time, 1, 500),
                   ('loca_Spectrum.json', time, 1, 500),
                   ('loca_Comcast.json', time, 1, 500),
                   ('loca_AT&T.json', time, 1, 500),
                   ('loca_Cox.json', time, 1, 500)]
        clustering(ISP_lst)

    time = ('2020-03-31', '2020-04-01')
    clustering([('loca_Verizon.json', time, 1, 500),
                ('loca_Spectrum.json', time, 1, 500),
                ('loca_Comcast.json', time, 1, 500),
                ('loca_AT&T.json', time, 1, 500),
                ('loca_Cox.json', time, 1, 500)])
