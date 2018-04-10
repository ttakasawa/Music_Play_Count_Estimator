from Code.Python.global_imports import *

song_data = csv_open(os.path.join(sql_results, 'artist_song_pairs.csv'))

tuple_data = []
for pair in song_data:
    tuple_data.append(tuple(pair))

sorted_data = sorted(tuple_data, key=lambda x: x[0])
write_csv_data(sorted_data, os.path.join(sql_results, 'sorted_artist_song_pairs.csv'), ',')
