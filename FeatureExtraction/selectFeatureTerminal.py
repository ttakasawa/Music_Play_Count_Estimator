import os
import re
import FeatureExtraction.audioSegmentation as Segment
import librosa
import numpy as np

media_dir = input("Enter the music directory:")
data_folder = input("Enter the destination directory:")

# Creates destination outer folder if nonexistent
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Read in selected songs into list and remove header

# Create split audio files
for song in os.listdir(media_dir):
    # Either regex will work, but split is possibly faster
    # name = re.findall("[0-9]*[^\.mp3]", song[song_title_index])
    print(song)
    name = re.split("\.", song)[0]
    in_file = os.path.join(media_dir, song)

    # Create song directories, load audio, and calculate number of segments
    audio_data, num_segments, song_path, segment_path = Segment.AudioSegmentationPrep(in_file, name, data_folder)

    # Iterate over number of segments
    for current_segment in range(0, num_segments):
        audio_segment_data = Segment.GetNextSegment(audio_data, current_segment)
        segment_file = Segment.SaveAudio(name, audio_segment_data, current_segment, segment_path)
        librosa_data, sample_rate = librosa.load(segment_file, sr=44100)
        # size: 221231

        np_save_files = re.split("\.", segment_file)[0]
        fft = librosa.stft(librosa_data, n_fft=4410)
        # n_fft = 4410  -> shape: 2206 x 201 size: 443406
        # n_fft = 44100 -> shape: 22051 x 21 size: 463071
        tempo = librosa.beat.tempo(librosa_data, sr=sample_rate)
        np.save(np_save_files + '_fft', fft)
        np.save(np_save_files + '_tempo', tempo)
    Segment.MoveOriginalFile(in_file, name, song_path)
