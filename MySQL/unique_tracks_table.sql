CREATE TABLE UniqueTracks
(
    unique_song_pk INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    track_id TINYTEXT,
    song_id TINYTEXT,
    artist_name TEXT,
    song_title TEXT
);
