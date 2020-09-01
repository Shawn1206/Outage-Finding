import json
from haversine import haversine
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt


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
    colors = [plt.cm.get_cmap('Spectral')(each) for each in np.linspace(0, 1,len(unique_labels))]
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

