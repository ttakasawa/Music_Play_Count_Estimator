from datetime import datetime
from Code.Python.SpotifyAPI.json_id_extraction import *
from Code.Python.global_imports import *


def json_extraction_setup():
    """
    This setup returns all the information needed to run the json ID extraction
    :return:
        delimiter - delimiter character for CSV file
        str_qualifier - text qualifier for CSV file
        start_dir - current directory
        output_file - string to file for saving data
        song_id_list - list of Echonest song IDs
        number_of_ids - count of ids in list
    """
    # Set delimiter and text qualifiers for CSV
    delimiter = '|'
    str_qualifier = ''

    # Save original directory
    start_dir = os.getcwd()
    output_file = os.path.join(json_extraction_results, "spotify_song_info.csv")

    # Open list of song IDs
    song_id_list = csv_open(os.path.join(sql_results, 'final_song_selection.csv'))

    # Extract song ID strings because the CSV populates a list of lists with a single item in each sublist
    song_id_list = [song_id[0] for song_id in song_id_list]
    number_of_ids = len(song_id_list)

    return delimiter, str_qualifier, start_dir, output_file, song_id_list, number_of_ids


def run_spotify_id_extraction(delimiter, str_qualifier, output_file, song_id_list, number_of_ids):
    """
    This function extracts the Artist, Song Title, and Spotify ID from the Echonest Mapping Archive:
    https://labs.acousticbrainz.org/million-song-dataset-echonest-archive/

    It then prints to a csv file: artist, song title, Spotify song ID, Echonest Song ID with the given delimiter

    :param delimiter: delimiter character for CSV file
    :param str_qualifier: text qualifier for CSV file
    :param output_file: string to file for saving data
    :param song_id_list: list of Echonest song IDs
    :param number_of_ids: count of ids in list
    :return: 1 if successful
    """
    # Move to data directory in order to search for json files
    os.chdir(os.path.join(data_directory, "millionsongdataset_echonest"))

    with open(output_file, 'w') as outfile:
        outfile.write("artist" + delimiter + "song" + delimiter + "spotify_id" + delimiter + "song_id\n")

    curr_id = 1
    for song_id in song_id_list:
        if (curr_id % 100 - 1) == 0:
            print(datetime.now().strftime("%H:%M:%S") + ": " + str(curr_id) + "/" + str(number_of_ids))
        file = os.path.abspath(os.popen("find ./ -name " + song_id + ".json").read().strip())
        song_json = LoadSongJSON(file)
        spotify_id, artist_name, song_name = ExtractSongInfo(song_json)
        with open(output_file, 'a') as outfile:
            outfile.write(
                str_qualifier + artist_name + str_qualifier + delimiter +
                str_qualifier + song_name + str_qualifier + delimiter +
                str_qualifier + spotify_id + str_qualifier + delimiter +
                str_qualifier + song_id + str_qualifier + "\n")
        curr_id += 1
    return 1


if __name__ == '__main__':
    # Run spotify ID extraction
    delim, str_qual, curr_dir, outfile, song_ids, num_ids = json_extraction_setup()
    run_spotify_id_extraction(delim, str_qual, outfile, song_ids, num_ids)
