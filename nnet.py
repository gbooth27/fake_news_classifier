
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
import numpy as np
import argparse
from keras.models import load_model
import parse_data
#from matplotlib import pyplot as plt
from keras import optimizers
import os
from keras import backend as K
import csv

def gen_training_data(data, examples):
    """
    formats data correctly
    :param data:
    :return:
    """

    author_dict = {}
    """author = 1
    for i in range(examples):
        # map each author to number
        if data[i][0] not in author_dict:
            author_dict[data[i][0]] = author
            author += 1
    """
    # Number of examples
    m = examples
    # Number of features
    n = len(data[0])-1
    x = np.zeros((m, n))
    y = np.zeros((m, 1))
    # get the data as numpy vectors
    for i in range(examples):
        for j in range(n):
            x[i][j] = data[i][j]
        y[i] = data[i][-1]

    return x, y

def predict(model, x, y):
    """
    predicts for x and calculates accuracy
    :param model:
    :param x:
    :param y:
    :return:
    """
    predict = model.predict(x=x)
    right = 0
    wrong = 0
    # calculate how accurate we are
    for i in range(len(predict)):
        if predict[i] < 0.5:
            curr = 0
        else:
            curr = 1
        # see if right or wrong
        if curr == y[i]:
            right += 1
        else:
            wrong += 1
    print("###############################")
    print("Number Correct: {}\nNumber Incorrect: {}\nPercent error: {}".format(right, wrong, 100*(wrong/len(predict))))
    print("###############################")


def run_nnet(data):
    """
    builds and runs the network
    :param data: examples
    :return:
    """
    x, y = gen_training_data(data, parse_data.N//2 + parse_data.N//3)

    model = Sequential()
    #dim1 = len(x)
    dim2 = len(x[0])
    # Add the layers.
    # Tuning
    model.add(Dense(dim2, input_dim=dim2, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dense(200, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dropout(0.2, noise_shape=None, seed=None))
    model.add(Dense(50, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dropout(0.2, noise_shape=None, seed=None))
    model.add(Dense(1000, kernel_initializer='random_uniform', activation='relu'))
    #model.add(Dropout(0.1, noise_shape=None, seed=None))
    #model.add(Dense(1000, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dropout(0.2, noise_shape=None, seed=None))
    model.add(Dense(1000, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dropout(0.2, noise_shape=None, seed=None))
    model.add(Dense(200, kernel_initializer='random_uniform', activation='relu'))
    #model.add(Dropout(0.2, noise_shape=None, seed=None))
    #model.add(Dense(1000, kernel_initializer='random_uniform', activation='relu'))
    #model.add(Dropout(0.1, noise_shape=None, seed=None))
    model.add(Dense(1, kernel_initializer='random_uniform', activation="relu"))
    sgd = optimizers.Adam()
    model.compile(loss='binary_crossentropy', optimizer=sgd)#, metrics=["mse"])

    model.fit(x, y, epochs=30, batch_size=100, verbose=2, validation_split=0.2)

    return model

if __name__ == "__main__":
    data = parse_data.parse("kaggle_data.csv")
    #with open("data_gen.csv", 'wb' ) as myfile:
       # wr = csv.writer(myfile, lineterminator='\n')
        #wr.writerows(data)

    model = run_nnet(data)
    x, y = gen_training_data(data[parse_data.N//2 + parse_data.N//3:], len(data[parse_data.N//2 + parse_data.N//3:]))
    print("Evaluating model...")
    evaluation = model.evaluate(x=x, y=y, verbose=2, batch_size=300)
    print("Test Loss: " + str(evaluation))
    print("\nPredicting against test data....")
    predict(model, x, y)
