from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
import numpy as np
import argparse
from keras.models import load_model
import parse_data
from keras import optimizers
import datetime


def gen_training_data(data, examples):
    """
    formats data correctly
    :param data: training data
    :param examples: number of examples to use
    :return: correctly formatted data
    """
    # Number of examples
    m = examples
    # Number of features
    n = len(data[0])-1
    x = np.zeros((m, n), dtype=np.float32)
    y = np.zeros((m, 1), dtype=np.float32)
    # get the data as numpy vectors
    for i in range(examples):
        for j in range(n):
            x[i][j] = data[i][j]
        y[i] = data[i][-1]

    return x, y


def gen_training_data2(data):
    """
    formats data correctly, for unlabeled examples
    :param data: unlabeled training data
    :return: correctly formatted data
    """
    # Number of examples
    m = len(data)
    # Number of features
    n = len(data[0])
    x = np.zeros((m, n), dtype=np.float32)
    #y = np.zeros((m, 1), dtype=np.float32)
    # get the data as numpy vectors
    for i in range(m):
        for j in range(n):
            x[i][j] = data[i][j]

    return x


def predict(model, x, y):
    """
    predicts for x and calculates accuracy
    :param model: model to predict against
    :param x: feature vectors
    :param y: labels
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
    print("Number Correct: {}\nNumber Incorrect: {}\nPercent accuracy: {}".format(right,
                                                                                  wrong,
                                                                                  100*(1-(wrong/len(predict)))))
    print("###############################")


def run_nnet(data):
    """
    builds and trains the network
    :param data: examples
    :return: trained model
    """
    #x, y = gen_training_data(data, parse_data.N//2 + parse_data.N//3)
    x, y = gen_training_data(data, parse_data.N-1)

    # THIS CODE WAS OUR ATTEMPT TO GET AROUND MEM REQS OF GPU, NOT ANY BETTER THAN NORMAL SADLY
    #val_split = 0.2
    #val_index = math.ceil(len(x)*(1-val_split))
    #training_gen = generator.generator(x[0:val_index],y[0:val_index])
    #val_gen = generator.generator(x[val_index:], y[val_index:])

    model = Sequential()
    #dim1 = len(x)
    dim2 = len(x[0])
    # Add the layers, Including dropout.
    model.add(Dense(dim2, input_dim=dim2, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dense(200, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dropout(0.1, noise_shape=None, seed=None))
    model.add(Dense(256, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dropout(0.1, noise_shape=None, seed=None))
    model.add(Dense(1000, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dense(200, kernel_initializer='random_uniform', activation='relu'))
    model.add(Dense(1, kernel_initializer='random_uniform', activation="relu"))
    # Set the optimizer
    opt = optimizers.Adam()
    model.compile(loss='binary_crossentropy', optimizer=opt)#, metrics=["mse"])
    # Print out the summary of the model
    print(model.summary())
    # Fit model, w/ validation split
    model.fit(x, y, epochs=15, batch_size=256, verbose=2, validation_split=0.2)

    return model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--text_only', "-t", dest='text_only', action='store_false',
                        help="Use to generate features using Only text data")
    args = parser.parse_args()


    data, data2  = parse_data.parse("kaggle_data.csv", "test.csv", args.text_only)

    # Train the model
    model = run_nnet(data)
    # Save the trained model
    model.save("models/model_" + datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".h5")

    print("\nPredicting against test FINAL data....")
    x = gen_training_data2(data2)
    predictions = model.predict(x=x)
    for i in range(len(predictions)):
        if predictions[i] > 0.5:
            predictions[i] = 1
        else:
            predictions[i] = 0

    np.savetxt("predictions.csv", predictions, delimiter=",", fmt='%1i',)


