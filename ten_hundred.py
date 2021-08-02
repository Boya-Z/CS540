import csv
import math
import numpy
from numpy import NaN
import copy


def load_data(filepath):
    data = []
    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        count = 0
        for row in reader:
            if count != 0:
                element = {'Province': row[0], 'Country': row[1], 'Cases': row[4:]}
                data.append(element)
            count += 1
    return data


def calculate_x_y(time_series):
    case1 = int(time_series['Cases'][len(time_series['Cases']) - 1]) / 10
    case2 = int(time_series['Cases'][len(time_series['Cases']) - 1]) / 100
    (x, y) = (NaN, NaN)
    for i in range(len(time_series['Cases']) - 1):
        if int(time_series['Cases'][i]) <= case1 < int(time_series['Cases'][i + 1]):
            x = i
        if int(time_series['Cases'][i]) <= case2 < int(time_series['Cases'][i + 1]):
            y = i
    if math.isnan(x):
        return x, y
    else:
        y = x - y
        x = len(time_series['Cases']) - x - 1
        return x, y


def hac(dataset):  # input exp: Afghanistan [(13, 25),(20, 23), (14, 29)]
    list = copy.deepcopy(dataset)  # remove NaN
    dataset.clear()
    for i in range(len(list)):
        if not (math.isnan(list[i][0]) or math.isnan(list[i][1])):
            dataset.append(list[i])

    orig_length = len(dataset)
    outer = []  # initial: 0 ... 244
    for num in range(len(dataset)):
        outer.append([num])

    min_dis = []  # the list contain all pair points with computed shortest distance
    Z = []
    if_skip = False
    tmp_min = float('inf')  # min distance record variable
    min_tup = ()
    if_potential = False
    for k in range(len(dataset) - 1):  # loop to clustering
        for i in range(len(dataset)):  # loop to compare distance
            for j in range(i + 1, len(dataset)):
                for md in min_dis:  # check if these two points have been added
                    if i in md and j in md:  # case: have been computed
                        if_skip = True
                        break
                for kk in range(len(outer)):
                    index = len(outer) - kk - 1
                    if len(outer[index]) == 1:  # these two points cannot in one cluster
                        break
                    if i in outer[index] and j in outer[index]:
                        if_skip = True
                        break
                if if_skip:
                    if_skip = False
                    continue  # compute distance of next pair of points
                # this pair have not been computed yet
                # compute distance between these two points
                cur_dis = math.sqrt(sum([(a - b) ** 2 for a, b in zip(dataset[i], dataset[j])]))
                if cur_dis < tmp_min:  # find shorter distance pair
                    tmp_min = cur_dis
                    min_tup = (i, j)
                if cur_dis == tmp_min:
                    cur_i = -1
                    cur_j = -1
                    recorded_i = -1
                    recorded_j = -1
                    for index1 in reversed(range(len(outer))):
                        if i in outer[index1]:
                            cur_i = index1
                            break
                    for index1 in reversed(range(len(outer))):
                        if j in outer[index1]:
                            cur_j = index1
                            break
                    for index1 in reversed(range(len(outer))):
                        if min_tup[0] in outer[index1]:
                            recorded_i = index1
                            break
                    for index1 in reversed(range(len(outer))):
                        if min_tup[1] in outer[index1]:
                            recorded_j = index1
                            break
                    aa = min(cur_i, cur_j)
                    bb = min(recorded_i, recorded_j)
                    cc = max(cur_i, cur_j)
                    dd = max(recorded_i, recorded_j)
                    if aa < bb or aa == bb and cc < dd:
                        min_tup = (i, j)
        # has found the shortest pair in this round
        min_dis.append(min_tup)
        cluster_num_i = -1
        # print(len(outer_cluster))
        for kk in range(len(outer)):
            index1 = len(outer) - kk - 1
            # print(str(i) + ' ' + str(kk) + ' ' + str(index1) + ' ' + str(outer_cluster[index1]))
            if min_tup[0] in outer[index1]:
                cluster_num_i = index1
                break
        cluster_num_j = -1
        for kk in range(len(outer)):
            index2 = len(outer) - kk - 1
            if min_tup[1] in outer[index2]:
                cluster_num_j = index2
                break
        num_points = len(outer[cluster_num_i]) + len(outer[cluster_num_j])
        element = [min(cluster_num_i, cluster_num_j), max(cluster_num_i, cluster_num_j), tmp_min, num_points]
        Z.append(element)
        new_points_set = outer[cluster_num_i] + outer[cluster_num_j]
        outer.append(new_points_set)

        # re-initialize for next loop
        tmp_min = float('inf')
        if_skip = False
    return numpy.asmatrix(Z)

raw_dataset = load_data("time_series_covid19_confirmed_global.csv")
dataset = []
for i in raw_dataset:
    dataset.append(calculate_x_y(i))
print(hac(dataset))