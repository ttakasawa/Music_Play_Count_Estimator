import numpy as np
from Code.Python.global_imports import *

spotify_id_location = 2
spotify_id_err = "!ERR: No Spotify Track ID Found"


def load_spotify_song_info(in_file):
    """
    Loads extracted spotify song IDs, pops off the header and returns the data
    :return:
        songs_raw - raw song data extracted with json extractor
        header - header of CSV file
    """
    songs_raw = csv_open(os.path.join(json_extraction_results, in_file), delim='|')
    header = songs_raw.pop(0)
    np_songs = np.array(songs_raw)

    # Verify dimensions of imported data are correct
    if len(np_songs.shape) != 2:
        exit(254)
        if np_songs.shape[1] != 4:
            exit(255)

    return songs_raw, header


def clean_spotify_data(song_data, header):
    """
    Removes all songs where spotify IDs couldn't be found from the list and returns the clean list with the header
    attached

    :param song_data: raw song data extracted with json extractor
    :param header: header of CSV file
    :return: list of cleaned song information
    """
    # Initialize list for song data with removed errors
    songs_cleaned = []
    for song in song_data:
        if song[spotify_id_location] != spotify_id_err:
            songs_cleaned.append(song)
    songs_cleaned = sorted(songs_cleaned)
    songs_cleaned.insert(0, header)
    return songs_cleaned


def join_spotify_data(spotify_song_data, song_ids, song_id_column):
    """
    Performs a SQL-like join on the data assuming a larger set of JSON information was extracted
    :param spotify_song_data: list of cleaned song information
    :param song_ids: list of Echonest song IDs from SQL queries
    :param song_id_column: column where Echonest song IDs are located in CSV
    :return: Joined list
    """
    join_result = []
    for song_id in song_ids:
        for song in spotify_song_data:
            if song[song_id_column] == song_id:
                join_result.append(song)
                break
    return join_result


if __name__ == "__main__":
    # Clean raw CSV from json extraction script
    raw_spotify_data, header = load_spotify_song_info('spotify_song_info_min_2_users.csv')
    cleaned_spotify_data = clean_spotify_data(raw_spotify_data, header)
    write_csv_data(cleaned_spotify_data, os.path.join(json_extraction_results, 'cleaned_spotify_songs_min_2_users.csv'),
                   delim='|')

    # Join on songs selected from SQL
    # sql_songs = csv_open(os.path.join(sql_results, 'final_song_selection.csv'))
    # sql_songs = [song_id[0] for song_id in sql_songs]
    # join_spotify_sql = join_spotify_data(cleaned_spotify_data, sql_songs, 3)
    # write_csv_data(join_spotify_sql, os.path.join(json_extraction_results, 'join_spotify_sql.csv'), delim='|')
