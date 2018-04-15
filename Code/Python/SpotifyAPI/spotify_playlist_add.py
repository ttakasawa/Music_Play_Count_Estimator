import json
import math
import re
from Code.Python.global_imports import *


def create_playlists(songs, songs_per_playlist, user_id, key):
    """
    Creates a set of playlists based on the number of songs that need to be added to lists
    :param songs: list of songs to be added
    :param songs_per_playlist: maximum number of songs allowed in each playlist
    :param key: api key loaded from text file in directory
    :return: list of created playlists
    """
    created_playlists = []
    curl_string_start = 'curl -X "POST" "https://api.spotify.com/v1/users/'
    curl_string_end = '/playlists" ' \
                      '--data "{' \
                      '\\"name\\":\\"PROJECT_PL_1\\",' \
                      '\\"description\\":\\"test\\",' \
                      '\\"public\\":false}" ' \
                      '-H "Accept: application/json" -H "Content-Type: application/json" ' \
                      '-H "Authorization: Bearer '

    add_playlist_curl_string = curl_string_start + user_id + curl_string_end + key + '"'

    max_playlists = int(math.ceil(len(songs) / songs_per_playlist) + 1)

    for i in range(1, max_playlists):
        curl_string = re.sub('PROJECT_PL_[0-9]*', 'PROJECT_PL_' + str(i), add_playlist_curl_string)
        playlist_json = os.popen(curl_string).read()
        print(playlist_json)
        playlist_json = json.loads(playlist_json)
        created_playlists.append([playlist_json.get('name'), playlist_json.get('id')])
    return created_playlists


def add_songs_to_playlist(playlists, songs, songs_per_playlist, user_id, key):
    """
    Adds the maximum allowed number of songs to a playlist given a list of songs.
    If all songs are added or the maximum number of songs allowed is reached.
    :param playlists: list of playlist IDs to add the songs to
    :param songs: list of songs to add
    :param songs_per_playlist: maximum number of songs allowed per playlist
    :param key: api key loaded from text file in directory
    :return: nothing
    """
    curl_string_begin = 'curl -X "POST" "https://api.spotify.com/v1/users/'
    curl_string_mid1 = '/playlists/'
    curl_string_mid2 = '/tracks?position=0&uris='
    curl_string_end = '" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer '

    offset = 0

    for playlist in playlists:
        add_song_string_start = curl_string_begin + user_id + curl_string_mid1 + playlist[1] + curl_string_mid2
        for i in range(offset, offset + songs_per_playlist, 10):
            if i >= len(songs):
                break
            else:
                song_id_string = ""
                for j in range(i, i + 11):
                    if j >= len(songs):
                        break
                    else:
                        song_id_string = song_id_string + 'spotify%3Atrack%3A' + songs[j][2] + '%2C'
                song_id_string = song_id_string[:-3]
                add_song_string = add_song_string_start + song_id_string + curl_string_end + key + '"'
                api_return = os.popen(add_song_string).read()
                print(api_return)
        offset += songs_per_playlist


if __name__ == '__main__':
    songs = csv_open(os.path.join(json_extraction_results, 'spotify_songs_sorted_no_errs.csv'), delim='|')
    songs.pop(0)
    max_songs_per_list = 9000
    with open('key.txt', 'r') as f:
        key = f.read()
    with open('user_id.txt', 'r') as f:
        user_id = f.read()
    playlists = create_playlists(songs, max_songs_per_list, user_id, key)
    add_songs_to_playlist(playlists, songs, max_songs_per_list, user_id, key)
