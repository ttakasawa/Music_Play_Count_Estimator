CREATE TABLE PlayRecords
(
  pk          INT AUTO_INCREMENT
    PRIMARY KEY,
  user_id     VARCHAR(40) NULL,
  song_id     VARCHAR(18) NULL,
  play_number INT         NULL
);

