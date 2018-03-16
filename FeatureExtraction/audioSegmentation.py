from __future__ import print_function
import librosa
from pydub import AudioSegment
import os


def split(input_file=librosa.util.example_audio_file(), name='sampleOutput', dest=os.getcwd(), step_size=5000,
          move_file=True):
    dir_path = os.path.join(dest, name)
    split_path = os.path.join(dir_path, 'split')

    # Create directory for song files if it doesn't exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Create directory for split audio files if it doesn't exist
    if not os.path.exists(split_path):
        os.makedirs(split_path)

    music = AudioSegment.from_file(input_file)
    num_segments = int(len(music) / step_size) + 1

    # splitting audio file into 5 seconds pieces

    for x in range(0, num_segments):
        start_point = step_size * x
        end_point = step_size * (x + 1)
        new_audio = music[start_point:end_point]
        rel_path = name + '_part_' + str(x) + '.mp3'
        output_path = os.path.join(split_path, rel_path)
        new_audio.export(output_path, format="mp3")

    if move_file:
        move(input_file, name, dir_path)


def move(input_file, name, dir_path):
    os.rename(input_file, os.path.join(dir_path, name + '.mp3'))
