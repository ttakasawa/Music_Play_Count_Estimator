import csv
import json
from Python.global_imports import *
from Python.SpotifyAPI.json_id_extraction import *
from datetime import datetime

# Save original directory
start_dir = os.getcwd()
output_file = os.path.join(json_extraction_results, "spotify_song_info.csv")

# Open list of song IDs
with open(os.path.join(sql_results, 'song_ids.csv')) as file:
    song_ids = list(csv.reader(file))

# Extract song ID strings because the CSV populates a list of lists with a single item in each sublist
song_ids = [song_id[0] for song_id in song_ids]
num_ids = len(song_ids)

# Move to data directory in order to search for json files
os.chdir(os.path.join(data_directory, "millionsongdataset_echonest"))

with open(output_file, 'w') as outfile:
    outfile.write("artist, song, spotify_id, song_id\n")

curr_id = 1
for song_id in song_ids:
    if (curr_id % 100 - 1) == 0:
        print(datetime.now().strftime("%H:%M:%S") + ": " + str(curr_id) + "/" + str(num_ids))
    file = os.path.abspath(os.popen("find ./ -name " + song_id + ".json").read().strip())
    song_json = LoadSongJSON(file)
    spotify_id, artist_name, song_name = ExtractSongInfo(song_json)
    with open(output_file, 'a') as outfile:
        delim = ''
        str_delim = '|'
        outfile.write(
            str_delim + artist_name + str_delim + delim +
            str_delim + song_name + str_delim + delim +
            str_delim + spotify_id + str_delim + delim +
            str_delim + song_id + str_delim + "\n")
    curr_id += 1