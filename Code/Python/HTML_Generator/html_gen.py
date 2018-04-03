import csv
from Python.global_imports import *

song_file_idx = 0
song_url_idx = 1
song_number = 0

html_1 = '<div class="panel panel-default"><div class="panel-body"><label>'
html_2 = '. Please rate the song from 1 to 10:<br /><br /><audio controls="" controlslist="nodownload"><source src="'
html_3 = '" type="audio/mpeg" /></audio></label><select class="form-control" name="Song'
html_4 = '"><option selected="selected" value="select one">- select one -</option><option value="0">0</option><option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option></select></div></div>'


with open(os.path.join(html_data, 'survey_song_links.csv'), 'r') as file:
    songs = list(csv.reader(file))

with open(os.path.join(html_results, 'survey_questions.html'), 'w') as html_file:
    for song in songs:
        song_number += 1
        song_url = song[song_url_idx]
        html_code = html_1 + (str)(song_number) + html_2 + song_url + html_3 + (str)(song_number) + html_4 + '\n'
        html_file.write(html_code)
