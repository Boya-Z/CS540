import csv
import math
import random

import numpy as np


# takes no arguments and returns the data as described below in an n-by-2 array
def get_dataset():
    results = []
    with open("winter_table.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:  # each row is a list
            results.append(row)
    for i in range(len(results)):
        if results[i][0] == '"':
            results[i - 1][1] = results[i][1]
    arr = np.array(results)
    index = []
    for j in range(len(arr)):
        if arr[j][0] == '"' or arr[j][1] == '---':
            index.append(j)
    arr = np.delete(arr, index, axis=0)
    arr = np.delete(arr, 0, axis=0)
    for k in arr:
        k[0] = k[0][:4]
    arr = arr.tolist()
    # for k in arr:
    # k = [int(i) for i in k]
    for i in range(0, len(arr)):
        for j in range(2):
            arr[i][j] = int(arr[i][j])
    return arr


# takes the dataset as produced by the previous function and prints several statistics about the data;
# does not return anything
def print_stats(dataset):
    num = len(dataset)
    print(num)
    sum = 0
    for i in range(0, num):
        sum = sum + dataset[i][1]
    mean = sum / num
    print("%.2f" % mean)
    diff = 0
    for i in range(0, num):
        diff = diff + pow(dataset[i][1] - mean, 2)
    s_d = math.sqrt(diff / (num - 1))
    print("%.2f" % s_d)


# calculates and returns the mean squared error on the dataset given fixed betas
def regression(beta_0, beta_1):
    dataset = get_dataset()
    sqr = 0
    for i in range(0, len(dataset)):
        sqr = sqr + pow(beta_0 + (dataset[i][0] * beta_1) - dataset[i][1], 2)
    ans = sqr / len(dataset)

    return round(ans, 2)


# performs a single step of gradient descent on the MSE and returns the derivative values as a tuple
def gradient_descent(beta_0, beta_1):
    dataset = get_dataset()
    sum1 = 0
    sum2 = 0
    for i in range(0, len(dataset)):
        sum1 = sum1 + beta_0 + (dataset[i][0] * beta_1) - dataset[i][1]
        sum2 = sum2 + (beta_0 + (dataset[i][0] * beta_1) - dataset[i][1]) * dataset[i][0]
    (gradient1, gradient2) = (round(sum1 * 2 / len(dataset), 2), round(sum2 * 2 / len(dataset), 2))
    return gradient1, gradient2


# performs T iterations of gradient descent starting at )( β 0 , β 1 ) = ( 0 , 0 )
# with the given parameter and prints the results; does not return anything
def iterate_gradient(T, eta):
    beta_0 = 0
    beta_1 = 0
    MSE = 0
    for i in range(1, T + 1):
        beta_0 = beta_0 - eta * gradient_descent(beta_0, beta_1)[0]
        beta_1 = beta_1 - eta * gradient_descent(beta_0, beta_1)[1]
        MSE = regression(beta_0, beta_1)

        print(i, end=" ")
        print("%.2f" % beta_0, end=" ")
        print("%.2f" % beta_1, end=" ")
        print("%.2f" % MSE)


# using the closed-form solution, calculates and returns the values of β 0 andβ 1 and the corresponding MSE
# as a three-element tuple
def compute_betas():
    dataset = get_dataset()
    sum_x = 0
    sum_y = 0
    sum_x_y = 0
    sum_x_sqr = 0
    for i in range(0, len(dataset)):
        sum_x = sum_x + dataset[i][0]
        sum_y = sum_y + dataset[i][1]
    mean_x = sum_x / len(dataset)
    mean_y = sum_y / len(dataset)
    for i in range(0, len(dataset)):
        sum_x_y = sum_x_y + (dataset[i][0] - mean_x) * (dataset[i][1] - mean_y)
        sum_x_sqr = sum_x_sqr + pow((dataset[i][0] - mean_x), 2)
    beta_1 = sum_x_y / sum_x_sqr
    beta_0 = mean_y - beta_1 * mean_x
    (beta_0, beta_1, MSE) = beta_0, beta_1, regression(beta_0, beta_1)
    return beta_0, beta_1, MSE


# using the closed-form solution betas, return the predicted number of ice days for that year
def predict(year):
    b0 = compute_betas()[0]
    b1 = compute_betas()[1]
    return round(b0 + b1 * year, 2)


def normalized_regression(beta_0, beta_1, data):
    sqr = 0
    for i in range(0, len(data)):
        sqr = sqr + pow(beta_0 + (data[i][0] * beta_1) - data[i][1], 2)
    ans = sqr / len(data)
    #return round(ans, 2)
    return ans


def normalized_gradient_descent(beta_0, beta_1, data):
    sum1 = 0
    sum2 = 0
    for i in range(0, len(data)):
        sum1 = sum1 + beta_0 + (data[i][0] * beta_1) - data[i][1]
        sum2 = sum2 + (beta_0 + (data[i][0] * beta_1) - data[i][1]) * data[i][0]
    (gradient1, gradient2) = (sum1 * 2 / len(data), sum2 * 2 / len(data))
    return gradient1, gradient2


# normalizes the data before performing gradient descent, prints results as in function 5
def iterate_normalized(T, eta):
    dataset = get_dataset()
    sum_x = 0
    sum_x_sqr = 0
    for i in range(0, len(dataset)):
        sum_x = sum_x + dataset[i][0]
    mean_x = sum_x / len(dataset)
    for i in range(0, len(dataset)):
        sum_x_sqr = sum_x_sqr + pow((dataset[i][0] - mean_x), 2)
    std_x = math.sqrt(sum_x_sqr / (len(dataset) - 1))
    for m in range(0, len(dataset)):
        dataset[m][0] = (dataset[m][0] - mean_x) / std_x

    beta_0 = 0
    beta_1 = 0
    MSE = 0
    for i in range(1, T + 1):
        beta_0 = beta_0 - eta * normalized_gradient_descent(beta_0, beta_1, dataset)[0]
        beta_1 = beta_1 - eta * normalized_gradient_descent(beta_0, beta_1, dataset)[1]
        MSE = normalized_regression(beta_0, beta_1, dataset)

        print(i, end=" ")
        print("%.2f" % beta_0, end=" ")
        print("%.2f" % beta_1, end=" ")
        print("%.2f" % MSE)

def sgd_gradient_descent(beta_0, beta_1,dataset,x,y):
    gradient1=beta_0 +x* beta_1-y
    gradient2=(beta_0 + x * beta_1 - y)*x

    (gradient1, gradient2) = (round(gradient1, 2), round(gradient2, 2))
    return gradient1, gradient2
# performs stochastic gradient descent, prints results as in function 5
def sgd(T, eta):
    dataset = get_dataset()
    sum_x = 0
    sum_x_sqr = 0
    for i in range(0, len(dataset)):
        sum_x = sum_x + dataset[i][0]
    mean_x = sum_x / len(dataset)
    for i in range(0, len(dataset)):
        sum_x_sqr = sum_x_sqr + pow((dataset[i][0] - mean_x), 2)
    std_x = math.sqrt(sum_x_sqr / (len(dataset) - 1))
    for m in range(0, len(dataset)):
        dataset[m][0] = (dataset[m][0] - mean_x) / std_x

    ran=random.randint(0, len(dataset)-1)
    beta_0 = 0
    beta_1 = 0
    MSE = 0
    for i in range(1, T + 1):
        beta_0 = beta_0 - eta * sgd_gradient_descent(beta_0, beta_1,dataset,dataset[ran][0],dataset[ran][1])[0]
        beta_1 = beta_1 - eta * sgd_gradient_descent(beta_0, beta_1,dataset,dataset[ran][0],dataset[ran][1])[1]
        MSE = normalized_regression(beta_0, beta_1, dataset)

        print(i, end=" ")
        print("%.2f" % beta_0, end=" ")
        print("%.2f" % beta_1, end=" ")
        print("%.2f" % MSE)
