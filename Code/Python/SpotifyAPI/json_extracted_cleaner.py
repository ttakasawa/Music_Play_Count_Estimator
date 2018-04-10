import numpy as np
from Code.Python.global_imports import *

spotify_id_location = 2
spotify_id_err = "!ERR: No Spotify Track ID Found"


def load_spotify_song_info():
    songs_raw = csv_open(os.path.join(json_extraction_results, 'spotify_song_info.csv'), delim='|')
    header = songs_raw.pop(0)
    np_songs = np.array(songs_raw)

    # Verify dimensions of imported data are correct
    if len(np_songs.shape) != 2:
        exit(254)
        if np_songs.shape[1] != 4:
            exit(255)

    return songs_raw, header


def clean_spotify_data(song_data, header):
    # Initialize list for song data with removed errors
    songs_cleaned = []
    for song in song_data:
        if song[spotify_id_location] != spotify_id_err:
            songs_cleaned.append(song)
    songs_cleaned = sorted(songs_cleaned)
    songs_cleaned.insert(0, header)
    return songs_cleaned


def join_spotify_data(spotify_song_data, song_ids, song_id_column):
    join_result = []
    for song_id in song_ids:
        for song in spotify_song_data:
            if song[song_id_column] == song_id:
                join_result.append(song)
                break
    return join_result


# Run Functions
raw_spotify_data, header = load_spotify_song_info()
cleaned_spotify_data = clean_spotify_data(raw_spotify_data, header)
sql_songs = csv_open(os.path.join(sql_results, 'final_song_selection.csv'))
sql_songs = [song_id[0] for song_id in sql_songs]
join_spotify_sql = join_spotify_data(cleaned_spotify_data, sql_songs, 3)
write_csv_data(cleaned_spotify_data, os.path.join(json_extraction_results, 'spotify_songs_sorted_no_errs.csv'),
               delim='|')
write_csv_data(join_spotify_sql, os.path.join(json_extraction_results, 'join_spotify_sql.csv'), delim='|')
