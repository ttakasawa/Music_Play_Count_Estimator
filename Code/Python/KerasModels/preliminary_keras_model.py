import os
import csv
import librosa
import numpy as np
from sklearn import preprocessing as pre
from keras.layers import LSTM, Dense
from keras.models import Sequential


def create_1D_model(time_steps):
    """
    Mono input signal, 5 seconds long: 1 clip x time_steps x 1 channel
    :param time_steps: length of each song segments
    :return: 1D LSTM model
    """
    model = Sequential()
    model.add(LSTM(1, input_shape=(time_steps, 1)))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='rmsprop', loss='mse')
    return model


def create_2D_model(time_steps):
    """
    Stereo input signal, 5 seconds long: 1 clip x time_steps x 2 channels
    :param time_steps: length of each song segments
    :return: 2D LSTM model
    """
    # Stereo input signal, 5 seconds long: 1 clip x time_steps x 2 channels
    model = Sequential()
    model.add(LSTM(1, input_shape=(time_steps, 2)))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='rmsprop', loss='mse')
    return model


def create_3D_model(time_steps, number_segments):
    """
    6 stereo input signals, each 5 seconds long: 6 clips x time_steps x 2 channels
    :param time_steps: length of each song segments
    :param number_segments: number of each song segments for each clip
    :return: 3D LSTM model
    """

    model = Sequential()
    model.add(LSTM(number_segments, input_shape=(time_steps, 2)))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='rmsprop', loss='mse')
    return model


def load_and_preprocess_user_data(user_file_path):
    """
    Loads and normalizes user play informaton to be used as targets for neural net
    :param user_file_path: Path to user song play records
    :return: Train and Test sets of data
    """
    # Open and load data from CSV
    with open(user_file_path, 'r') as file:
        unprocessed_data = np.array(list(csv.reader(file)))

    # Extract song IDs and number of plays for those songs for user
    song_ids = unprocessed_data[:, 1]
    plays = unprocessed_data[:, 2].astype(int).reshape(-1, 1)

    # Normalize and Standardize data
    plays_norm = pre.normalize(plays, axis=0, norm='max')
    plays_std = pre.robust_scale(plays)

    # Reassemble into matrix
    processed_data = np.column_stack((song_ids, plays, plays_norm, plays_std))

    # Split data into training and test sets
    np.random.shuffle(processed_data)
    num_train = np.floor(processed_data.shape[0] * 0.8).astype(int)

    # Return train and test sets
    return processed_data[0:num_train, ], processed_data[num_train:, ]


def load_music_segment(music_file_path, monophonic=False):
    librosa_data, sample_rate = librosa.load(music_file_path, mono=monophonic)
    if librosa_data.shape[0] < time_steps:
        librosa_data = np.pad(librosa_data, (0, time_steps - librosa_data.shape[0]), 'constant',
                              constant_values=(0, 0))
    return librosa_data


def load_music_3D(song_segment_path, song_id, segment_start, segment_end):
    """
    Given a start segment and end segment, creates a matrix that's: num_segments x segment length x 2 channels
    :param song_segment_path: path to song segments
    :param song_id: Echonest ID of song
    :param segment_start: first segment to load
    :param segment_end: last segment to load
    :return: matrix of audio clip data
    """
    base_string = song_id + '_part_'
    song_data = []
    for segment in range(segment_start, segment_end + 1):
        segment_name = base_string + str(segment) + '.mp3'
        segment_data = load_music_segment(os.path.join(song_segment_path, segment_name))
        if segment == segment_start:
            song_data = segment_data.T
        else:
            song_data = np.dstack((song_data, segment_data.T))
    return song_data


def transform_1D_data(data):
    data_1D = np.expand_dims(data, 0)
    data_1D = np.expand_dims(data_1D, 2)
    return data_1D


def run_2D_model():
    pass


def run_3D_model():
    pass


if __name__ == '__main__':
    time_steps = 222336 / 2
    data_dim = 1
    idx = 0

    # Fit models
    # lstm_1D.fit(data_1D, np.array([1]))  # 1 x 111168, x 1 -> 1x1
    # lstm_2D.fit(data1_stereo.T, np.array([1]))  # 1 x 111168, x 2 -> 1x1
    # lstm_3D.fit(data_3D, np.array([1, 1, 1, 1, 1, 1]))  # 6 x 111168, x 2 -> 6 x 1 -> 1x1
