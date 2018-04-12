import os
import librosa
import numpy as np
from keras.layers import LSTM, Dense
from keras.models import Sequential

time_steps = 222336
data_dim = 1

model = Sequential()
model.add(LSTM(1, input_shape=(time_steps, data_dim)))
model.add(Dense(1, activation='linear'))
model.compile(optimizer='rmsprop', loss='mse')

y_train = np.array([[[0]], [[1]], [[1]], [[1]], [[1]], [[1]], [[0]], [[0]], [[1]], [[1]], [[1]], [[0]]])
y_test = np.array([[0, 1, 1, 1, 0]])

idx = 0

data_location = '/media/kyle/Storage/survey_songs_extracted'
for folder in os.listdir(data_location):
    segment_path = os.path.join(data_location, folder, 'split')
    for segment in os.listdir(segment_path):
        segment_file = os.path.join(segment_path, segment)
        librosa_data, sample_rate = librosa.load(segment_file, sr=44100)
        if librosa_data.shape[0] < time_steps:
            librosa_data = np.pad(librosa_data, (0, time_steps - librosa_data.shape[0]), 'constant',
                                  constant_values=(0, 0))
        librosa_data = np.expand_dims(librosa_data, 0)
        librosa_data = np.expand_dims(librosa_data, 2)
        model.fit(librosa_data, y_train[idx])
    idx += 1

###########
# Testing #
###########
import librosa
import numpy as np
from keras.layers import LSTM, Dense
from keras.models import Sequential

data1_mono, sr = librosa.load('clip_10.0.mp3')
data1_stereo, sr = librosa.load('clip_10.0.mp3', mono=False)
data2_stereo, sr = librosa.load('clip_11.0.mp3', mono=False)
data3_stereo, sr = librosa.load('clip_12.0.mp3', mono=False)
data4_stereo, sr = librosa.load('clip_13.0.mp3', mono=False)
data5_stereo, sr = librosa.load('clip_14.0.mp3', mono=False)
data6_stereo, sr = librosa.load('clip_15.0.mp3', mono=False)

data_3D = np.array([data1_stereo.T, data2_stereo.T, data3_stereo.T, data4_stereo.T, data5_stereo.T, data6_stereo.T])

time_steps = data1_mono.shape[0]


# Mono input signal, 5 seconds long: 1 clip x time_steps x 1 channel
lstm_1D = Sequential()
lstm_1D.add(LSTM(1, input_shape=(time_steps, 1)))
lstm_1D.add(Dense(1, activation='linear'))
lstm_1D.compile(optimizer='rmsprop', loss='mse')
data_1D = np.expand_dims(data1_mono, 0)
data_1D = np.expand_dims(data_1D, 2)

# Stereo input signal, 5 seconds long: 1 clip x time_steps x 2 channels
lstm_2D = Sequential()
lstm_2D.add(LSTM(1, input_shape=(time_steps, 2)))
lstm_2D.add(Dense(1, activation='linear'))
lstm_2D.compile(optimizer='rmsprop', loss='mse')

# 6 stereo input signals, each 5 seconds long: 6 clips x time_steps x 2 channels
lstm_3D = Sequential()
lstm_3D.add(LSTM(6, input_shape=(time_steps, 2)))
lstm_3D.add(Dense(1, activation='linear'))
lstm_3D.compile(optimizer='rmsprop', loss='mse')


# Fit models
lstm_1D.fit(data_1D, np.array([1])) # 1 x 111168, x 1 -> 1x1
lstm_2D.fit(data1_stereo.T, np.array([1])) # 1 x 111168, x 2 -> 1x1
lstm_3D.fit(data_3D, np.array([1, 1, 1, 1, 1, 1])) # 6 x 111168, x 2 -> 6 x 1 -> 1x1