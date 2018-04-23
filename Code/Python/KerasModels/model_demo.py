import os
import sys
import csv
import librosa
import numpy as np
from sklearn import preprocessing as pre
from keras.models import load_model

def load_and_preprocess_user_data(user_data_file_path, audio_file_path):
    """
    Loads and normalizes user play informaton to be used as targets for neural net
    :param user_data_file_path: Path to user song play records
    :return: Train and Test sets of data
    """
    np.random.seed(1)
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
    np.random.shuffle(processed_data)
    return processed_data


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


def load_music(song_segment_path, user_data, song_id_idx, target_idx, segment_len, time_steps=24):
    """
    Loads music in a (num_songs, num_segments, len_segments) numpy array and targets as (num_songs, 1) NP array
    :param song_segment_path: path to segment files
    :param user_data: preprocessed user data
    :param song_id_idx: index of song ID in user data
    :param target_idx: index of target value in user data
    :param segment_len: length of all segments
    :param time_steps: number of segments to load per song
    :return: music and target numpy arrays
    """
    target_array = []
    music_data = False
    for data in user_data:
        song_id = data[song_id_idx]
        song_dir = os.path.join(song_segment_path, song_id)
        print("LOADING SONG: " + song_id)
        sys.stdout.flush()
        # Set number of times song should be split
        segments = sorted(os.listdir(song_dir))
        num_splits = int(np.floor(len(segments) / time_steps))
        # Iterate over number of splits
        for i in range(0, num_splits):
            # Set target
            target_array.append(data[target_idx])
            split_data = False
            # Set begin and end of segment splitting
            first_segment = i * time_steps
            last_segment = i * time_steps + time_steps
            # Load segments into memory and append to split_data
            for j in range(first_segment, last_segment):
                segment_path = os.path.join(song_dir, segments[j])
                segment_data = load_music_segment(segment_path, segment_len, True)
                segment_data = np.reshape(segment_data, (1, 1, len(segment_data)))
                # Check if split song data has been initialized with NP array
                if isinstance(split_data, bool):
                    split_data = segment_data
                else:
                    split_data = np.column_stack((split_data, segment_data))
            # Check if music data has been initialized with NP array
            if isinstance(music_data, bool):
                music_data = split_data
            else:
                music_data = np.vstack((music_data, split_data))
    return music_data, np.array(target_array)

if __name__ == '__main__':

    segment_length = int(222336 / 2)
    song_index = 0  # Echonest song ID values
    target_index = 3  # Standardized values
    user_data_file = os.path.join(os.getcwd(), 'user_data/user_2.csv')
    music_dir = os.path.join(os.getcwd(), 'split_songs/')

    user_data = load_and_preprocess_user_data(user_data_file, music_dir)
    user_data = [user_data[0]]
    music = []
    targets = []
    music, targets = load_music(music_dir, user_data, song_index, target_index, segment_length, 22)

    print("======================================================")
    print("=== LOADING MODEL: USER 2, 2 LSTM LAYERS, 22 STEPS ===")
    print("======================================================")
    model = load_model('user_2_22-Steps_2-Layer.h5')
    print("======================================================")
    print("=== EVAULUATING MODEL                              ===")
    print("======================================================")
    print("MSE: " + str(model.evaluate(music, targets)))