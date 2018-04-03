USE DS340_Project;

###############################################################
## USER PLAY THRESHOLD
###############################################################
SELECT user_id, song_id, plays
FROM PlayRecords
WHERE plays > 201
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