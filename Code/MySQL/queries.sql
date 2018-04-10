USE DS340_Project;

###############################################################
## USER PLAY THRESHOLD
###############################################################
SELECT user_id, song_id, plays
FROM PlayRecords
WHERE plays < 201
ORDER BY song_id;

###############################################################
## USER PLAY COUNTS
###############################################################

## Get total play counts from each user
SELECT user_id, SUM(plays) AS total_user_playcount
FROM PlayRecords
WHERE plays < 201
GROUP BY user_id
ORDER BY total_user_playcount DESC;

#### IMPORTED NEW TABLE AS RESULT OF ABOVE QUERY

## Check Number of Users given Play Threshold
SELECT UserPlaycounts.user_id, UserPlaycounts.total_user_playcount
FROM UserPlaycounts
WHERE UserPlaycounts.total_user_playcount > 1612
      AND UserPlaycounts.total_user_playcount < 6000
ORDER BY UserPlaycounts.total_user_playcount DESC;

## Get all songs listened to from above users
SELECT PlayRecords.user_id, PlayRecords.song_id, PlayRecords.plays
FROM PlayRecords
  INNER JOIN (SELECT UserPlaycounts.user_id, UserPlaycounts.total_user_playcount
              FROM UserPlaycounts
              WHERE UserPlaycounts.total_user_playcount > 1612
                    AND UserPlaycounts.total_user_playcount < 6000) AS TopUsers
    ON TopUsers.user_id = PlayRecords.user_id
WHERE plays < 201
ORDER BY plays DESC;

#### IMPORTED NEW TABLE AS RESULT OF ABOVE QUERY


###############################################################
## USER PLAY RECORD AGGREGATES
###############################################################
SELECT DISTINCT song_id
FROM TopUserPlayRecords;
# 101823 songs

SELECT DISTINCT user_id
FROM TopUserPlayRecords;

SELECT UniqueTracks.artist_name, UniqueTracks.song_title
FROM UniqueTracks,
  (SELECT DISTINCT TopUserPlayRecords.song_id
   FROM TopUserPlayRecords) unique_songs
WHERE UniqueTracks.song_id = unique_songs.song_id;


SELECT UniqueTracks.artist_name, UniqueTracks.song_title
FROM UniqueTracks,
  (SELECT DISTINCT TopUserPlayRecords.song_id
   FROM TopUserPlayRecords) unique_songs
WHERE UniqueTracks.song_id = unique_songs.song_id
INTO OUTFILE '/home/kyle/git/UnsupervisedDeepMusicRecommendation/MySQL/Results/artist_song_pairs.csv'
FIELDS TERMINATED BY ','
  ENCLOSED BY '"'
LINES TERMINATED BY '\n';

###############################################################
## Narrow Down Songs Chosen
###############################################################

# SELECT SONGS LISTENED TO BY 50 OR MORE USERS
CREATE VIEW aggregate_song_counts AS
SELECT song_id, COUNT(user_id) AS total_users
FROM TopUserPlayRecords
GROUP BY song_id
HAVING total_users >= 50
ORDER BY total_users DESC;

# Get top users with highest total playcounts for these songs
CREATE VIEW selected_users AS
SELECT TopUserPlayRecords.user_id, SUM(TopUserPlayRecords.plays) total_user_playcounts
FROM TopUserPlayRecords, aggregate_song_counts
WHERE aggregate_song_counts.song_id = TopUserPlayRecords.song_id
GROUP BY TopUserPlayRecords.user_id
HAVING total_user_playcounts > 1800
ORDER BY total_user_playcounts DESC;

# GET UNIQUE RECORDS FOR THESE SONG, USER PAIRS
SELECT PlayRecords.user_id, PlayRecords.song_id, PlayRecords.plays
FROM PlayRecords, aggregate_song_counts, selected_users
WHERE selected_users.user_id = PlayRecords.user_id
      AND PlayRecords.song_id = aggregate_song_counts.song_id;

# GET LIST OF ALL SONGS LISTENED TO BY TOP 5 USERS WITH A TOTAL OF 50+ PLAYS AMONGST ALL USERS
SELECT DISTINCT Top5_User_Records.song_id
FROM  Top5_User_Records;

# GET LIST OF ALL SONGS LISTENED TO BY TOP 5 USERS IGNORING MINIMUM PLAYS
SELECT DISTINCT PlayRecords.song_id
FROM PlayRecords, selected_users
WHERE selected_users.user_id = PlayRecords.user_id;