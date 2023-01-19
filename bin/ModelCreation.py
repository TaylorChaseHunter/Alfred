"""
    As taken from the model testing notebook. Sets an lstm model to training for a set amount
    of time.
"""
import os
import pandas as pd
import numpy as np
import configparser
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical


class ModelCreator:
    """
        A basic frame class to contain the LSTM model creation
    """

    def __init__(self):

        parser = configparser.ConfigParser()
        parser.read('../config.ini')

        self.num_of_layers = parser.getint('Model', 'HiddenLayers')
        self.layer_size = parser.getint('Model', 'LayerSize')

        self.X = None
        self.y = None

    def train(self) -> None:
        self.load_and_clean_data()
        self.create_model()

    def load_and_clean_data(self) -> None:
        """
            Load the pickled data and create the class variables needed to train
            the model.
        """

        dataframe = pd.read_pickle('../data/quotes.pkl')
        dataframe = dataframe.drop(['Author', 'Tags'], axis=1)
        dataframe = dataframe.apply(lambda x: x.astype(str).str.lower())
        quotes = dataframe['Quote'].to_list()
        combined_quotes = " ".join(quotes)

        chars = sorted(list(set(combined_quotes)))
        c = ['\n', '\r', ' ', '!', '"', "'", '(', ')', '*', ',', '-', '.', ':', ';', '?', '[', ']', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '\xbb', '\xbf', '\xef']
        updated_quotes = [x for x in combined_quotes if x in c]
        updated_quotes = ''.join(updated_quotes)

        n_chars = len(updated_quotes)
        n_vocab = len(chars)
        char_to_int = dict((c, i) for i, c in enumerate(chars))

        seq_length = 100
        dataX = []
        dataY = []

        for i in range(0, n_chars - seq_length, 1):
            seq_in = updated_quotes[i:i + seq_length]
            seq_out = updated_quotes[i + seq_length]
            dataX.append([char_to_int[char] for char in seq_in])
            dataY.append(char_to_int[seq_out])
        n_patterns = len(dataX)

        # reshape X to be [samples, time steps, features]
        X = np.reshape(dataX, (n_patterns, seq_length, 1))
        # normalize
        self.X = X / float(n_vocab)
        # one hot encode the output variable
        self.y = to_categorical(dataY)

    def create_model(self) -> None:
        """
            Create the basic LSTM model and fit it.
        """

        # define the LSTM model
        model = Sequential()

        for layer in range(self.num_of_layers):
            model.add(LSTM(self.layer_size, input_shape=(self.X.shape[1], self.X.shape[2])))

        model.add(Dropout(0.2))
        model.add(Dense(self.y.shape[1], activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')

        # define the checkpoint
        filepath = "weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
        checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
        callbacks_list = [checkpoint]

        model.fit(self.X, self.y, epochs=3, batch_size=246, callbacks=callbacks_list)


creator = ModelCreator
creator.train()
