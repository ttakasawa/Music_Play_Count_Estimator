import json
import re


def LoadSongJSON(path):
    with open(path, 'r') as file:
        song_json = json.load(file)
    return song_json


def ExtractSongInfo(song_json):
    spotify_id = "!ERR: No Spotify Track ID Found"
    artist_name = "!ERR: No artist name found"
    song_name = "!ERR: No song name found"
    if 'response' in song_json.keys():
        json_data = song_json.get('response')
        if 'songs' in json_data.keys():
            json_data = json_data.get('songs')
            if len(json_data) > 0:
                json_data = json_data[0]
                if 'artist_name' in json_data.keys():
                    artist_name = json_data.get('artist_name')
                if 'title' in json_data.keys():
                    song_name = json_data.get('title')
                if 'tracks' in json_data.keys():
                    json_data = json_data.get('tracks')
                    for id_json in json_data:
                        if id_json.get('catalog') == 'spotify':
                            spotify_id = (re.split(':', id_json.get('foreign_id'))[2])

    return spotify_id, artist_name, song_name
