import os
import sys
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


def load_and_preprocess_user_data(user_data_file_path, audio_file_path):
    """
    Loads and normalizes user play informaton to be used as targets for neural net
    :param user_data_file_path: Path to user song play records
    :return: Train and Test sets of data
    """
    # Open and load data from CSV
    with open(user_data_file_path, 'r') as file:
        unprocessed_data = np.array(list(csv.reader(file)))

    # Remove non-existing songs from data records
    music_folders = os.listdir(audio_file_path)
    to_remove = []
    for i in range(0, unprocessed_data.shape[0]):
        song = unprocessed_data[i, :]
        if song[1] not in music_folders:
            to_remove.append(i)

    unprocessed_data = np.delete(unprocessed_data, to_remove, axis=0)
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


def load_music_segment(music_file_path, t_steps, monophonic=False):
    """
    Loads and returns a 5 second segment of audio
    :param music_file_path: path of actual mp3 file
    :param t_steps: number of time steps numpy array should be
    :param monophonic: determines whether it should load mono or stereo signal
    :return: np array of music data from librosa
    """
    librosa_data, sample_rate = librosa.load(music_file_path, mono=monophonic)

    # Ensure stereo audio clips are ACTUALLY stereo, not mono
    if not monophonic:
        if librosa_data.ndim == 1:
            librosa_data = np.expand_dims(librosa_data, 0)
        if librosa_data.shape[0] == 1:
            librosa_data = np.repeat(librosa_data, 2, axis=0)

    # If audio clip is too short, pad zeros
    if librosa_data.ndim == 1:
        if librosa_data.shape[0] < t_steps:
            pad_value = t_steps - librosa_data.shape[0]
            librosa_data = np.pad(librosa_data, (0, pad_value), mode='constant', constant_values=0)
    elif librosa_data.ndim == 2:
        if librosa_data.shape[1] < t_steps:
            pad_value = t_steps - librosa_data.shape[1]
            librosa_data = np.pad(librosa_data, ((0, 0), (0, pad_value)), mode='constant', constant_values=0)
    return librosa_data


def load_music_3D(song_segment_path, t_steps, song_id, segment_start, segment_end):
    """
    Given a start segment and end segment, creates a matrix that's: num_segments x segment length x 2 channels
    :param song_segment_path: path to song segments
    :param t_steps: number of time steps numpy array should be
    :param song_id: Echonest ID of song
    :param segment_start: first segment to load
    :param segment_end: last segment to load
    :return: matrix of audio clip data
    """
    base_string = song_id + '_part_'
    song_data = []
    for segment in range(segment_start, segment_end + 1):
        segment_name = base_string + str(segment) + '.mp3'
        segment_data = load_music_segment(os.path.join(song_segment_path, segment_name), t_steps)
        if segment == segment_start:
            song_data = segment_data
        else:
            song_data = np.dstack((song_data, segment_data))
    return song_data.T


def transform_1D_data(data):
    """
    Transforms the 1D mono data into an acceptable dimensionality for keras
    :param data: 1D numpy array
    :return: 3D numpy array of 1, time_steps, 1
    """
    data_1D = np.expand_dims(data, 0)
    data_1D = np.expand_dims(data_1D, 2)
    return data_1D


def transform_2D_data(data):
    """
    Transforms the 2D stereo data into an acceptable dimensionality for keras
    :param data: 2D numpy array
    :return: 3D numpy array of 1, time_steps, 2
    """
    data_2D = np.expand_dims(data.T, 0)
    return data_2D


def train_2D_model(t_steps, song_id_idx, target_idx, train_data, audio_dir):
    """
    Trains a 2-Dimensional, single layer LSTM model using keras
    :param t_steps: number of time steps for each audio segment
    :param song_id_idx: index location of song IDs in user data
    :param target_idx: index location of target values in user data
    :param train_data: array of user data to use as training data
    :param audio_dir: directory that audio files are located
    :return: trained 2D model
    """
    lstm_2D = create_2D_model(t_steps)
    for sample in train_data:
        print("TRAINING ON SAMPLE: " + sample[song_id_idx])
        target = np.array([sample[target_idx].astype('float64')])
        song_dir = os.path.join(audio_dir, sample[song_id_idx])
        for segment in os.listdir(song_dir):
            music_data = load_music_segment(os.path.join(song_dir, segment), t_steps)
            music_data = transform_2D_data(music_data)
            lstm_2D.fit(music_data, target)
    return lstm_2D


def validate_2D_model(trained_model, t_steps, song_id_idx, target_idx, test_data, audio_dir):
    """
    Performs MSE accuracy testing on a trained 2D LSTM model
    :param trained_model: reference to trained keras model object
    :param t_steps: number of time steps each audio segment should be
    :param song_id_idx: index location of song IDs in user data
    :param target_idx: index location of target values in user data
    :param test_data: array of user data to use as testing data
    :param audio_dir: directory that audio files are located
    :return: mean squared error for predictions
    """
    error = np.float64(0.0)
    num_segments = 0
    for sample in test_data:
        print("TESTING ON SAMPLE: " + sample[song_id_idx])
        target = np.array([sample[target_idx].astype('float64')])
        song_dir = os.path.join(audio_dir, sample[song_id_idx])
        for segment in os.listdir(song_dir):
            num_segments += 1
            music_data = load_music_segment(os.path.join(song_dir, segment), t_steps)
            music_data = transform_2D_data(music_data)
            prediction = trained_model.predict(music_data)
            error += np.square(target - prediction)
    return error / num_segments


def train_3D_model(t_steps, song_id_idx, target_idx, train_data, audio_dir):
    """
    Trains a 3-Dimensional, single layer LSTM model using keras with a total of 30 seconds of audio per training step
    :param t_steps: number of time steps for each audio segment
    :param song_id_idx: index location of song IDs in user data
    :param target_idx: index location of target values in user data
    :param train_data: array of user data to use as training data
    :param audio_dir: directory that audio files are located
    :return: trained 3D model
    """
    lstm_3D = create_3D_model(t_steps, 6)
    for sample in train_data:
        print("TRAINING ON SAMPLE: " + sample[song_id_idx])
        target = np.array([sample[target_idx].astype('float64')]) * np.ones(6)
        music_data = load_music_3D(os.path.join(audio_dir, sample[song_id_idx]), t_steps, sample[song_id_idx], 5, 10)
        lstm_3D.fit(music_data, target)
    return lstm_3D


def validate_3D_model(trained_model, t_steps, song_id_idx, target_idx, test_data, audio_dir):
    """
    Performs MSE accuracy testing on a trained 2D LSTM model
    :param trained_model: reference to trained keras model object
    :param t_steps: number of time steps each audio segment should be
    :param song_id_idx: index location of song IDs in user data
    :param target_idx: index location of target values in user data
    :param test_data: array of user data to use as testing data
    :param audio_dir: directory that audio files are located
    :return: mean squared error for predictions
    """
    error = np.float64(0.0)
    num_segments = 0
    for sample in test_data:
        print("TESTING ON SAMPLE: " + sample[song_id_idx])
        target = np.array([sample[target_idx].astype('float64')]) * np.ones(6)
        num_segments += 1
        music_data = load_music_3D(os.path.join(audio_dir, sample[song_id_idx]), t_steps, sample[song_id_idx], 5, 10)
        prediction = trained_model.predict(music_data)
        error_vector = np.square(target - prediction)
        error += error_vector.sum()
    return error / num_segments


if __name__ == '__main__':
    error_string = "Incorrect usage. \n" \
                   "Call 'keras_model.py n_dim' where n_dim is 2 for the 2D model or 3 for the 3D model"
    if len(sys.argv) != 2:
        print(error_string, file=sys.stderr)
        exit(-55)
    elif sys.argv[1] != '2' and sys.argv[1] != '3':
        print(error_string, file=sys.stderr)
        exit(-55)
    # Set variables for running model
    time_steps = int(222336 / 2)
    song_index = 0  # Echonest song ID values
    target_index = 3  # Standardized values
    user_data_dir = os.path.join(os.getcwd(), 'user_data/')
    music_dir = os.path.join(os.getcwd(), 'split_songs/')

    # Run model
    for user in range(1, 6):
        user_file = os.path.join(user_data_dir, "user_" + str(user) + ".csv")
        train_data, test_data = load_and_preprocess_user_data(user_file, music_dir)

        if sys.argv[1] == '2':
            # 2D model
            model_accuracy_file = 'model_accuracies_2D.csv'
            model_name = 'user_' + str(user) + '_2D_model.h5'
            with open(model_accuracy_file, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['model_name', 'accuracy'])

            print("TRAINING 2D MODEL")
            trained_model = train_2D_model(time_steps, song_index, target_index, train_data, music_dir)
            accuracy = validate_2D_model(trained_model, time_steps, song_index, target_index, test_data, music_dir)

        else:
            # 3D model
            model_accuracy_file = 'model_accuracies_3D.csv'
            model_name = 'user_' + str(user) + '_3D_model.h5'
            with open(model_accuracy_file, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['model_name', 'accuracy'])

            print("TRAINING 3D MODEL")
            trained_model = train_3D_model(time_steps, song_index, target_index, train_data, music_dir)
            accuracy = validate_3D_model(trained_model, time_steps, song_index, target_index, test_data, music_dir)

        # Save model

        trained_model.save(os.path.join(os.getcwd(), model_name))
        with open(model_accuracy_file, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([model_name, accuracy])
