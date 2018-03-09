
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
import numpy as np
import argparse
from keras.models import load_model
import parse_data
from matplotlib import pyplot as plt
from keras import optimizers
import os
from keras import backend as K

def gen_training_data(data):
    """
    formats data correctly
    :param data:
    :return:
    """

    examples = 10000
    author_dict = {}
    author = 1
    for i in range(examples):
        # map each author to number
        if data[i][0] not in author_dict:
            author_dict[data[i][0]] = author
            author += 1

    m = examples
    n = 1
    x = np.zeros((m, n))
    y = np.zeros((m, 1))
    for i in range(examples):
        x[i] = author_dict[data[i][0]]
        y[i] = data[i][1]

    return x, y


def run_nnet(data):
    """
    builds and runs the network
    :param data: examples
    :return:
    """
    x, y = gen_training_data(data)

    model = Sequential()
    dim1 = len(x)
    dim2 = len(x[0])
    # Add the layers.
    # Tuning
    model.add(Dense(dim1, input_dim=dim2, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dense(200, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dense(400, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dropout(0.1, noise_shape=None, seed=None))
    model.add(Dense(1000, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dense(200, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dropout(0.1, noise_shape=None, seed=None))
    model.add(Dense(1, kernel_initializer='random_uniform', activation="tanh"))
    sgd = optimizers.Adam()
    model.compile(loss='mse', optimizer=sgd)

    model.fit(x, y, epochs=2, batch_size=512, verbose=2, validation_split=0.2)

    return model

if __name__ == "__main__":
    model = run_nnet(parse_data.parse("kaggle_data.csv"))
    title_data, text_data, author_data = parse_data("kaggle_data.csv")

    x, y = gen_training_data(author_data)
    print("Evaluating model...")
    evaluation = model.evaluate(x=x, y=y, verbose=1, batch_size=300)
    print("accuracy: " +str(evaluation))
    #print("Loss(mse): {}  metrics MAE: {} err : {}".format(*evaluation))