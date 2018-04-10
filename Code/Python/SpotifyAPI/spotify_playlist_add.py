import json
import math
import re
from Code.Python.global_imports import *

songs = csv_open(os.path.join(json_extraction_results, 'join_spotify_sql.csv'), delim='|')
songs.pop(0)

with open('key.txt', 'r') as f:
    key = f.read()

# Create Playlists to be Used
songs_per_playlist = 9000
created_playlists = [['test', '1'], ['test', '2'], ['test', '3'], ['test', '4'], ['test', '5'], ['test', '6'],
                     ['test', '7'], ['test', '8'], ['test', '9']]

add_playlist_curl_string = 'curl -X "POST" "https://api.spotify.com/v1/users/ty6ox21rodfvlrg1poba0i6fz/playlists" ' \
                           '--data "{' \
                           '\\"name\\":\\"PROJECT_PL_1\\",' \
                           '\\"description\\":\\"test\\",' \
                           '\\"public\\":false}" ' \
                           '-H "Accept: application/json" -H "Content-Type: application/json" ' \
                           '-H "Authorization: Bearer '

add_playlist_curl_string = add_playlist_curl_string + key + '"'

max_playlists = int(math.ceil(len(songs) / songs_per_playlist) + 1)

for i in range(1, max_playlists):
    curl_string = re.sub('PROJECT_PL_[0-9]*', 'PROJECT_PL_' + str(i), add_playlist_curl_string)
    playlist_json = os.popen(curl_string).read()
    playlist_json = json.loads(playlist_json)
    created_playlists.append([playlist_json.get('name'), playlist_json.get('id')])

# Add songs to playlist
add_song_string_begin = 'curl -X "POST" "https://api.spotify.com/v1/users/ty6ox21rodfvlrg1poba0i6fz/playlists/'
add_song_string_middle = '/tracks?position=0&uris='
add_song_string_end = '-H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer '

offset = 0

for playlist in created_playlists:
    add_song_string = add_song_string_begin + playlist[1] + add_song_string_middle
    for i in range(offset, offset + songs_per_playlist, 100):
        if i > len(songs):
            break
        else:
            song_id_string = ""
            for j in range(i, i + 100):
                if j > len(songs):
                    break
                else:
                    # ERROR FROM LINE BELOW HERE
                    song_id_string = song_id_string + 'spotify%3Atrack%' + songs[j][2] + '%2C'
                    print(songs[j][2])
            add_song_string = add_song_string + song_id_string + add_song_string_end + key + '"'
            os.popen(add_song_string)
    offset += songs_per_playlist
