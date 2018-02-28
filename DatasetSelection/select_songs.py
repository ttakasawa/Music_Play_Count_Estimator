import csv
import json
import re


def clear():
    print("\n" * 250)


## Set areas for data allocation
track_data = []
genres = []

# Set columns to get from CSV file
columns = [0, 5, 2, 37, 27]
# column [0] = File Name
# column [5] = Artist Name
# column [2] = Album Title
# column [37] = Song Title
# column [27] = Genre

## Set constants to be used throughout script
max_songs = 20
csv_genre_column = 27

track_data_id_column = 0
track_data_artist_column = 1
track_data_album_column = 2
track_data_track_column = 3
track_data_genre_column = 4
selected_for_column = 5

genre_name_column = 0

actual_songs = {}
with open('./actual_songs.txt', 'r') as file:
    for song_id in file:
        actual_songs[int(song_id)] = 1

with open('./fma_metadata/raw_tracks.csv', 'r') as file:
    tracks = csv.reader(file)
    run = 0
    for track in tracks:
        track_info = []
        for column in columns:
            data = track[column]
            if column == csv_genre_column and run == 1:
                data = re.findall("(?<=genre_title': ').*?[^']*", data)
                # Regex explanation:
                # ? - Looks for this character or set of chars
                # . - Looks for any non-whitespace char
                # * - Looks for any number of repetitions
                # "(?<=)" finds any string that starts with whatever comes after the <=
                # "?[^']*" stops searching and excludes last character if character is a single quote
                for genre in data:
                    genres.append(genre)
            track_info.append(data)
        if run == 0 or int(track[track_data_id_column]) in actual_songs:
            track_data.append(track_info)
        if run == 0:
            run = 1

genres = set(genres)
genres = sorted(genres)
genres = dict.fromkeys(genres, 0)

for song in range(1, len(track_data)):
    for genre in track_data[song][track_data_genre_column]:
        genres[genre] += 1

genre_tuples = []
for genre, count in genres.items():
    if count > max_songs:
        genre_tuples.append((genre, count))

genre_tuples.sort(key=lambda x: x[1])

selected_songs = []
selected_song_dict = {}
for genre in genre_tuples:
    count = 0
    for song in track_data:
        for song_genre in song[track_data_genre_column]:
            if count < max_songs:
                if song_genre == genre[genre_name_column]:
                    if song[track_data_id_column] not in selected_song_dict:
                        selected_song_dict[song[track_data_id_column]] = 1
                        temp = song
                        temp.append(song_genre)
                        selected_songs.append(temp)
                        count += 1
                        break
            else:
                break

with open('./songs_to_copy.sh', 'w') as outfile:
    outfile.write("#!/bin/bash\n")
    outfile.write("mp3_files=(\n")
    for song_id in selected_song_dict:
        outfile.write("    '{0:0>6}.mp3'".format(int(song_id)) + "\n")
    outfile.write("    )\n")

with open('./selected_songs.csv', 'w') as outfile:
    outfile.write('file,artist,album,track,genres,selected_for\n')
    for song in selected_songs:
        song_file_name = "{0:0>6}.mp3".format(int(song[track_data_id_column]))
        song_artist = re.sub(",", ";", str(song[track_data_artist_column]))
        song_album = re.sub(",", ";", str(song[track_data_album_column]))
        song_name = re.sub(",", ";", str(song[track_data_track_column]))
        song_genres = re.sub(",", ";", str(song[track_data_genre_column]))
        song_selected_for = re.sub(",", ";", str(song[selected_for_column]))
        outfile.write(song_file_name + "," +
                      song_artist + "," +
                      song_album + "," +
                      song_name + "," +
                      song_genres + "," +
                      song_selected_for + "\n")

with open('./genre_counts.csv', 'w') as outfile:
    for genre, count in sorted(genres.items()):
        outfile.write(genre + "," + str(count) + "\n")
