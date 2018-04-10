import csv
from Python.global_imports import *
import numpy as np

spotify_id_location = 2
spotify_id_err = "!ERR: No Spotify Track ID Found"
with open(os.path.join(json_extraction_results, 'spotify_song_info.csv'), 'r') as file:
    songs_raw = list(csv.reader(file, delimiter='|'))
    np_songs = np.array(songs_raw)

    # Verify dimensions of imported data are correct
    if len(np_songs.shape) != 2:
        exit(254)
        if np_songs.shape[1] != 4:
            exit(255)

    # Initialize list for song data with removed errors
    songs_cleaned = []
    for song in songs_raw:
        if song[spotify_id_location] != spotify_id_err:
            songs_cleaned.append(song)
    songs_cleaned = sorted(songs_cleaned)

with open(os.path.join(json_extraction_results, 'spotify_songs_sorted_no_errs.csv'), 'w') as outfile:
    writer = csv.writer(outfile, delimiter='|')
    for song in songs_cleaned:
        writer.writerow(song)
