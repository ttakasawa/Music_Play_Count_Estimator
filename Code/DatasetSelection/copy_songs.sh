#!/bin/bash
source songs_to_copy.sh

rm -rf ../selected_songs
mkdir -p ../selected_songs

for i in "${!mp3_files[@]}"
    do 
        song=${mp3_files[$i]}
		find . -iname $song -exec cp -t ../selected_songs {} +
    done
