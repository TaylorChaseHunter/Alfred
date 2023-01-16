"""
    As taken from the model testing notebook
"""
import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical

df = pd.read_pickle('data/quotes.pkl')
df = df.drop(['Author', 'Tags'], axis=1)
df = df.apply(lambda x: x.astype(str).str.lower())
quotes = df['Quote'].to_list()
concatted_quotes = " ".join(quotes)

chars = sorted(list(set(concatted_quotes)))
c = ['\n', '\r', ' ', '!', '"', "'", '(', ')', '*', ',', '-', '.', ':', ';', '?', '[', ']', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '\xbb', '\xbf', '\xef']
updated_quotes = [x for x in concatted_quotes if x in c]

chars = sorted(list(set(updated_quotes)))
updated_quotes = ''.join(updated_quotes)

n_chars = len(updated_quotes)
n_vocab = len(chars)

chars = sorted(list(set(updated_quotes)))
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
X = X / float(n_vocab)
# one hot encode the output variable
y = to_categorical(dataY)

# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# define the checkpoint
filepath = "weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model.fit(X, y, epochs=3, batch_size=246, callbacks=callbacks_list)
