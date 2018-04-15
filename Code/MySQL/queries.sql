USE DS340_Project;

###############################################################
## THRESHOLD MAX PLAYS PER RECORD
###############################################################
# Create a view of all play records with 200 or less plays
DROP VIEW truncated_records;
CREATE VIEW truncated_records AS
  SELECT user_id, song_id, plays
  FROM PlayRecords
  WHERE plays < 201
  ORDER BY song_id;

###############################################################
## NARROW DOWN TO TOP 5 USERS BASED ON PLAY COUNTS
###############################################################

## Get total play counts from each user
DROP VIEW user_play_counts;
CREATE VIEW user_play_counts AS
  SELECT user_id, SUM(plays) AS total_user_playcount
  FROM truncated_records
  GROUP BY user_id
  ORDER BY total_user_playcount DESC;

#### CREATED NEW TABLE FROM ABOVE VIEW

## Get list of users given a minimum number of plays
DROP VIEW users_min_plays;
CREATE VIEW users_min_plays AS
  SELECT UserPlaycounts.user_id, UserPlaycounts.total_user_playcount
  FROM UserPlaycounts
  WHERE UserPlaycounts.total_user_playcount > 1612
  ORDER BY UserPlaycounts.total_user_playcount DESC;

# Get top 5 users by number of plays
DROP VIEW top_5_users;
CREATE VIEW top_5_users AS
  SELECT UserPlaycounts.user_id, UserPlaycounts.total_user_playcount
  FROM UserPlaycounts
  ORDER BY UserPlaycounts.total_user_playcount DESC
  LIMIT 5;

###############################################################
## Narrow Down Songs Chosen
###############################################################

# Get list of songs listened to by the top 5 users
DROP VIEW top_user_play_records;
CREATE VIEW top_user_play_records AS
  SELECT truncated_records.user_id, truncated_records.song_id, truncated_records.plays
  FROM truncated_records, top_5_users
  WHERE top_5_users.user_id = truncated_records.user_id
  ORDER BY plays DESC;

# Get total play counts for songs listened to by top 5 users.
DROP VIEW top_song_plays;
CREATE VIEW top_song_plays AS
  SELECT song_id, SUM(plays) AS total_song_plays
  FROM top_user_play_records, top_5_users
  WHERE top_user_play_records.user_id = top_5_users.user_id
  GROUP BY song_id
  ORDER BY total_song_plays DESC;

# Get unique list of songs from top played songs
SELECT DISTINCT song_id
FROM top_song_plays;
