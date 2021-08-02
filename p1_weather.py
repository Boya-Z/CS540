# import the math module
import math

#return the Euclidean distance between two dictionary data points from the data set.
def euclidean_distance(data_point1, data_point2):
    x1 = math.pow(data_point1.get('PRCP') - data_point2.get('PRCP'), 2)
    x2 = math.pow(data_point1.get('TMAX') - data_point2.get('TMAX'), 2)
    x3 = math.pow(data_point1.get('TMIN') - data_point2.get('TMIN'), 2)
    distance = math.sqrt(x1 + x2 + x3)
    return distance

#return a list of data point dictionaries read from the specified file.
def read_dataset(filename):
    file = open(filename, "r")
    datalist = []
    for line in file:
        d = {}
        data = line.split()
        d['DATE'] = data[0]
        d['PRCP'] = float(data[1])
        d['TMAX'] = float(data[2])
        d['TMIN'] = float(data[3])
        d['RAIN'] = data[4]
        datalist.append(d)
    return datalist

#return a prediction of whether it is raining or not based on a majority vote of the list of neighbors.
def majority_vote(nearest_neighbors):
    t = 'TRUE'
    f = 'FALSE'
    rain = [d['RAIN'] for d in nearest_neighbors]
    i = len(nearest_neighbors) - 1
    count = 0
    while i >= 0:
        if rain[i] == f:
            count = count + 1
        i = i - 1

    if len(nearest_neighbors) % 2 != 0:
        major = int(len(nearest_neighbors) // 2) + 1
        if count >= major:
            return f
        else:
            return t
    else:
        major1 = len(nearest_neighbors) / 2
        if count > major1:
            return f
        else:
            return t

#using the above functions, return the majority vote prediction for whether it's raining or not on the
# provided test point.
def k_nearest_neighbors(filename, test_point, k):
    datalist = read_dataset(filename)
    t = 'TRUE'
    f = 'FALSE'
    if test_point.get('PRCP') == 0.00:
        return f
    distances= list()
    for i in range(len(datalist)):
        dis = euclidean_distance(datalist[i], test_point)
        distances.append((datalist[i], dis))
    distances.sort(key=lambda tup: tup[1])
    neighbors = list()
    for j in range(k):
        neighbors.append(distances[j][0])
    return majority_vote(neighbors)

