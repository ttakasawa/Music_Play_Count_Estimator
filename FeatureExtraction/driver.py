import os
import csv
import re
import FeatureExtraction.audioSegmentation as AS

song_title_index = 0
media_dir = input("Enter the music directory:")
destination_path = input("Enter the destination directory:")

# Creates destination outer folder if nonexistent
if not os.path.exists(destination_path):
    os.makedirs(destination_path)

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
    AS.split(in_file, name, destination_path)
