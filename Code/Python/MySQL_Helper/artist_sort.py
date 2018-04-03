import csv
from Python.global_imports import *


with open(os.path.join(sql_results, 'artist_song_pairs.csv'), 'r') as file:
    reader = csv.reader(file)
    song_data = list(reader)

tuple_data = []
for pair in song_data:
    tuple_data.append(tuple(pair))

sorted_data = sorted(tuple_data, key=lambda x: x[0])

with open(os.path.join(sql_results, 'sorted_artist_song_pairs.csv'), 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['artist', 'song'])
    for pair in sorted_data:
        csv_out.writerow(pair)
