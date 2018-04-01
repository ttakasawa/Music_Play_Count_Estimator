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

###############################################################
## USER PLAY RECORD AGGREGATES
###############################################################
SELECT DISTINCTd song_id
FROM TopUserPlayRecords;

SELECT DISTINCT user_id
FROM TopUserPlayRecords;
