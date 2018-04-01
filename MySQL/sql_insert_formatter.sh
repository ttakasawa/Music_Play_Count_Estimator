#!/bin/bash

# Convert CSV to SQL insert statements
x=1
for file in ./split/*; do
    echo "USE DS340_Project;" > "./insert_statements/sql_insert_"$x".sql"
    echo "INSERT INTO PlayRecords (user_id, song_id, play_number) VALUES" >> "./insert_statements/sql_insert_"$x".sql"
    awk 'BEGIN{ FS=OFS="<SEP>" }{ print "('\''"$1"'\'','\''"$2"'\'','\''"$3"'\'','\''"$4"'\'')," }' $file >> "./insert_statements/sql_insert_"$x".sql"
    x=$((x+1))
done

# Convert unique track id file into SQL insert statement
x=1
for file in ./split/*; do
    echo "USE DS340_Project;" > "./insert_statements/unique_tracks_"$x".sql"
    echo "INSERT INTO UniqueTracks (track_id, song_id, artist_name, song_title) VALUES" >> "./insert_statements/unique_tracks_"$x".sql"
    awk 'BEGIN{ FS=OFS="<SEP>" }{ print "('\''"$1"'\'','\''"$2"'\'','\''"$3"'\'','\''"$4"'\'')," }' $file >> "./insert_statements/unique_tracks_"$x".sql"
    x=$((x+1))
done

# Replace last comma with semicolon in every insert statement file
for file in ./insert_statements/*; do
    sed -i '$ s/.$/;/' $file
done
