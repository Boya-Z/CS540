import re, glob, os
from collections import OrderedDict, Counter
import math


# loads the training data, estimates the prior distribution P(label) and class conditional distributions
# )P ( w o r d ∣ l a b e l ), return the trained model
def train(training_directory, cutoff):
    vocab = create_vocabulary(training_directory, cutoff)
    training_data = load_training_data(vocab, training_directory)
    p = prior(training_data, ['2016', '2020'])
    output16 = p_word_given_label(vocab, training_data, '2016')
    output20 = p_word_given_label(vocab, training_data, '2020')
    dic = {'vocabulary': vocab, 'log prior': p, 'log p(w|y=2016)': output16, 'log p(w|y=2020)': output20}
    return dic


# create and return a vocabulary as a list of word types with counts >= cutoff in the training directory
def create_vocabulary(training_directory, cutoff):
    # collect all the files with `.txt` extension
    subdir1 = os.listdir(training_directory + './2020')
    subdir2 = os.listdir(training_directory + './2016')
    # concatenate files
    cat_content = []
    for file in subdir1:
        with open(training_directory + '2020/' + file, 'r') as f:
            content = f.read()
            cat_content.append(content)
    for file in subdir2:
        with open(training_directory + '2016/' + file, 'r') as f:
            content = f.read()
            cat_content.append(content)

    contents = "\n".join(cat_content)
    # extract the words
    words = re.findall(r"\S+", contents)
    words = [word.lower() for word in words]
    words_counter = Counter(words)
    # words_counter = OrderedDict(sorted(words_counter.items(), key=lambda t: t[1], reverse=True))
    words_counter = sorted(words_counter.items(), key=lambda t: t[1], reverse=True)
    # print(words_counter)
    vocab = []
    for k, v in words_counter:
        if v >= cutoff:
            vocab.append(k)
    vocab.sort()
    # print(vocab)
    return vocab


# create and return a bag of words Python dictionary from a single document
def create_bow(vocab, filepath):
    bow = []
    f = open(filepath, 'r')
    content = f.read()
    words = re.findall(r"\S+", content)
    words = [word.lower() for word in words]
    words_counter = Counter(words)
    # words_counter = (words_counter.items(), key=lambda t: t[1])
    # words_counter = sorted(words_counter.items())
    # words_counter=dict(words_counter)
    words_counter = words_counter.items()
    # print(words_counter)
    count = 0
    # index=0
    for i in words_counter:
        if i[0] in vocab:
            bow.append(i)
        elif i not in vocab:
            count = count + int(i[1])
        # index=index+1
    bow = dict(bow)
    if count > 0:
        # bow.append(None)
        bow[None] = count
    return bow


# create and return training set (bag of words Python dictionary + label) from the files in a training directory
def load_training_data(vocab, directory):
    training_data = []
    subdir1 = os.listdir(directory + './2016')
    subdir2 = os.listdir(directory + './2020')
    for file1 in subdir1:
        dic = {}
        dic['label'] = '2016'
        dic['bow'] = create_bow(vocab, directory + '2016/' + file1)
        training_data.append(dic)
    for file2 in subdir2:
        dic = {}
        dic['label'] = '2020'
        dic['bow'] = create_bow(vocab, directory + '2020/' + file2)
        training_data.append(dic)
    return training_data


# given a training set, estimate and return the prior probability p(label) of each label
def prior(training_data, label_list):
    num1 = 0
    num2 = 0
    for i in training_data:
        if i.get('label') == label_list[0]:
            num1 = num1 + 1
        elif i.get('label') == label_list[1]:
            num2 = num2 + 1
    p1 = math.log((num1) / len(training_data))
    p2 = math.log((num2) / len(training_data))
    dic = {}
    dic[label_list[0]] = p1
    dic[label_list[1]] = p2
    # print(dic)
    return dic


# given a training set and a vocabulary, estimate and return the class conditional distribution
# log P ( w o r d ∣ l a b e l ) over all words for the given label using smoothing

def p_word_given_label(vocab, training_data, label):
    dic = {}
    n = 1
    sum_up = 0
    for i in vocab:
        dic[i] = 1
    for i in training_data:
        if i.get('label') == label:
            for key in i.get('bow'):
                if key in vocab:
                    dic[key] = dic[key] + i.get('bow')[key]
                if key not in vocab:
                    n = n + i.get('bow')[key]

        dic[None] = n
    for k in dic:
        sum_up = sum_up + dic[k]
    # print(sum_up)
    for word in dic:
        dic[word] = math.log(dic[word] / (sum_up))

    # print(dic)
    return dic


# given a trained model, predict the label for the test document (see below for implementation details including return value)
# this high-level function should also use create_bow(vocab, filepath)
def classify(model, filepath):
    log_prior = {}
    log_prior = model.get('log prior')
    l_p16 = log_prior.get('2016')
    l_p20 = log_prior.get('2020')
    vocab = model.get('vocabulary')
    count = create_bow(vocab, filepath)
    pwy_16 = model.get('log p(w|y=2016)')
    pwy_20 = model.get('log p(w|y=2020)')
    sum_16 = l_p16
    sum_20 = l_p20
    for i in pwy_16:
        if i in count:
            sum_16 = sum_16 + pwy_16.get(i) * count.get(i)
    for j in pwy_20:
        if j in count:
            sum_20 = sum_20 + pwy_20.get(j) * count.get(j)
    if max(sum_20, sum_16) == sum_16:
        pred = '2016'
    else:
        pred = '2020'

    result = {'log p(y=2020|x)': sum_20, 'log p(y=2016|x)': sum_16, 'predicted y': pred}
    return result
