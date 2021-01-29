# this script is used for convert location names to coordinates
import datetime
import json
from geonamescache import GeonamesCache
from constant import state_dict, state_list, capital_dic, directions

def geo_match2(location_names):
    """
    This function match US city names with corresponding coordinates
    :param location_names: str, content of input file
    :return: str
    """
    def data_preprocess(data):
        """
        this function preprocess the input data, change the format and datatype of timestamp, and add multiple
        location names into a single list
        :param data: json dict
        :return: json dict
        """
        data_formal = {}
        for i in data:
            time = datetime.datetime.strptime(i[:19], "%Y-%m-%dT%H:%M:%S")
            # the pattern of timestamp could vary for different data source
            data_formal[str(time)] = [j[0] for j in data[i][0]]
        return data_formal

    location_names = data_preprocess(location_names)
    output = {}
    # load the coordinates items into a dictionary called new_data
    bad_items = []
    gc = GeonamesCache()
    state_dic_abbr = gc.get_us_states()
    new_data = {'DC': [38.895, -77.0366667], 'St. Paul': [44.9537, -93.0900], 'Temcula': [33.4936, -117.1484]}
    with open("city_loca.json", 'r') as f2:  # load coordinates from data source
        for line in f2:
            datum = json.loads(line)
            if datum['CityNameAccented'] not in new_data:
                new_data[datum['CityNameAccented']] = [datum['Latitude'], datum['Longitude']]
    # traverse through the extracted location names
    for i in location_names:
        s = len(output)
        for name in location_names[i]:
            if name:
                new = name.split(' ')  # split by space
            else:
                new = []
            name = ''
            for j in range(len(new)):
                if new[j] and new[j] != ' ':
                    new[j] = new[j][0].upper() + new[j][1:]  # capitalize the word
                name += new[j]
                if j != len(new) - 1:
                    name += ' '

            if name in new_data:  # deal common cases
                output[i] = new_data[name]
                break

            if name.split(' ')[-1] in state_list:  # deal with situation like "New York NY"
                separator = ' '
                name_city = separator.join(name.split(' ')[:-1])
                if name_city in new_data:
                    output[i] = new_data[name_city]
                    break

            if name.split(' ')[0] in directions:  # deal with situation like "South west NY"
                separator = ' '
                name_city = separator.join(name.split(' ')[1:])
                if name_city in new_data:
                    output[i] = new_data[name_city]
                    break
                else:
                    continue

        if i not in output:  # if the above method failed to match coordinates
            full_state_name = ''
            for name in location_names[i]:
                if name:
                    new = name.split(' ')
                else:
                    new = []
                name = ''
                for j in range(len(new)):
                    if new[j] and new[j] != ' ':
                        new[j] = new[j][0].upper() + new[j][1:]
                    name += new[j]
                    if j != len(new) - 1:
                        name += ' '
                if name in state_dic_abbr:
                    full_state_name = state_dic_abbr[name]['name']  # use the state name instead
                else:
                    if name in capital_dic:
                        full_state_name = name
                if full_state_name:
                    tmp0 = capital_dic[full_state_name]  # use capital city to match coordinates
                    try:
                        output[i] = new_data[tmp0]
                        break
                    except:
                        continue
        e = len(output)
        if s == e:
            bad_items.append((i, location_names[i]))  # record the location names that can't be converted
    print(bad_items)
    with open('coordinates_IstheServicedown_' + 'Verizon' + '.json', 'w') as outfile:
        json.dump(output, outfile)
    return 'done'



if __name__ == '__main__':
    f = open('loca_IstheServiceDown_verizon.json')
    data = json.load(f)
    print(len(data))
    print(len(geo_match2(data)))
