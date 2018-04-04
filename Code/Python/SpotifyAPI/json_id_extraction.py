import re
import json


def LoadSongJSON(path):
    with open(path, 'r') as file:
        song_json = json.load(file)
    return song_json


def ExtractSpotifyID(song_json):
    foreign_ids = song_json.get('response').get('songs')[0].get('artist_foreign_ids')
    for id_json in foreign_ids:
        if id_json.get('catalog') == 'spotify':
            print(re.split(':', id_json.get('foreign_id'))[2])

# test = os.popen("find . -maxdepth 1 -name Downloads").read().strip()
