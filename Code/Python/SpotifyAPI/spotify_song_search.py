import csv
import json
from Python.global_imports import *
from Python.SpotifyAPI.json_id_extraction import *


with open(os.path.join(sql_results, 'artist_song_pairs.csv')) as file:
    artist_song_pairs = list(csv.reader(file))
