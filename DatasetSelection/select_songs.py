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

with open('./fma_metadata/raw_tracks.csv', 'r') as file:
    tracks = csv.reader(file)
    run = 0
    for track in tracks:
        track_info = []
        for column in columns:
            data = track[column]
            if column == 27 and run == 1:
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
        if run == 0: run = 1
        track_data.append(track_info)

genres = set(genres)
genres = sorted(genres)
genres = dict.fromkeys(genres, 0)

for song in range(1, len(track_data)):
    for genre in track_data[song][4]:
        genres[genre] += 1

with open('./genre_counts.csv', 'w') as outfile:
    for genre, count in sorted(genres.items()):
        outfile.write(genre + "," + str(count) + "\n")
