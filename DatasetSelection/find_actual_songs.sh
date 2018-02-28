#!/bin/bash

find . -iname "*.mp3" | gawk '{ split($0, a, "[/.]", seps); print a[4]}' > actual_songs.txt

