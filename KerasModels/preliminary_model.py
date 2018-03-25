import os
import numpy as np
import librosa
import keras
from keras.models import Sequential
from keras.layers import LSTM, Dense

time_steps = 222336
data_dim = 1

model = Sequential()
model.add(LSTM(1, input_shape=(time_steps, data_dim)))
model.add(Dense(1, activation='linear'))
model.compile(optimizer='rmsprop', loss='mse')

y_train = [0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0]
y_test = [0, 1, 1, 1, 0]

idx = 0

data_location = '/media/kyle/Storage/testing_data/train'
for folder in os.listdir(data_location):
    segment_path = os.path.join(data_location, folder, 'split')
    for segment in os.listdir(segment_path):
        segment_file = os.path.join(segment_path, segment)
        librosa_data, sample_rate = librosa.load(segment_file, sr=44100)
        print(librosa_data.shape)
        if librosa_data.shape[0] < time_steps:
            librosa_data = np.pad(librosa_data, (0, time_steps - librosa_data.shape[0]), 'constant',
                                  constant_values=(0, 0))
        librosa_data = librosa_data[:, np.newaxis, np.newaxis]
        model.fit(librosa_data, y_train[idx])
    idx += 1

# Current error: Error when checking input: expected lstm_1_input to have shape (222336, 1)
# but got array with shape (1, 1)

# I think the input array needs to be dim (1, time_steps, 1)
