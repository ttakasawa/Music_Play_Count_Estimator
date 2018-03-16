from __future__ import print_function
import librosa
from pydub import AudioSegment
import os


def split(input_file=librosa.util.example_audio_file(), name='sampleOutput', dest=os.getcwd(), step_size=5000):
    if not os.path.exists(os.path.join(dest, name)):
        os.makedirs(os.path.join(dest, name))

    music = AudioSegment.from_file(input_file)
    num_segments = int(len(music) / step_size) + 1

    # splitting audio file into 5 seconds pieces

    for x in range(0, num_segments):
        start_point = step_size * x
        end_point = step_size * (x + 1)
        new_audio = music[start_point:end_point]
        rel_path = name + '_part_' + str(x) + '.mp3'
        output_path = os.path.join(dest, name, rel_path)
        new_audio.export(output_path, format="mp3")


split('/media/kyle/17E798DB35D99867/blah/000002.mp3', '000002', '/media/kyle/17E798DB35D99867/blah/')
