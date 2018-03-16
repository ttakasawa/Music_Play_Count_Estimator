import os
import csv
import re
import FeatureExtraction.audioSegmentation as Segment

song_title_index = 0
media_dir = input("Enter the music directory:")
data_folder = input("Enter the destination directory:")

# Creates destination outer folder if nonexistent
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

# Read in selected songs into list and remove header
with open('../DatasetSelection/selected_songs.csv', 'r') as file:
    reader = csv.reader(file)
    selected_songs = list(reader)
selected_songs.pop(0)

# Create split audio files
for song in selected_songs:
    # Either regex will work, but split is possibly faster
    # name = re.findall("[0-9]*[^\.mp3]", song[song_title_index])
    name = re.split("\.", song[song_title_index])[0]
    in_file = os.path.join(media_dir, song[song_title_index])

    # Create song directories, load audio, and calculate number of segments
    audio_data, num_segments, song_path, segment_path = Segment.AudioSegmentationPrep(in_file, name, data_folder)

    # Iterate over number of segments
    for current_segment in range(0, num_segments):
        audio_segment_data = Segment.GetNextSegment(audio_data, current_segment)
        Segment.SaveAudio(name, audio_segment_data, current_segment, segment_path)
