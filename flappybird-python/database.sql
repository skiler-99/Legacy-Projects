CREATE DATABASE flappy_game;
USE flappy_game;

CREATE TABLE leaderboard (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(50),
    score INT
);
-- Insert sample record
INSERT INTO leaderboard (player_name, score) VALUES ('SamplePlayer', 5);
