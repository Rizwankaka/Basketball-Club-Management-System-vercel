-- Create Users table
CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128)
);

-- Create Players table
CREATE TABLE IF NOT EXISTS player (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    height FLOAT NOT NULL,
    position VARCHAR(20) NOT NULL
);

-- Create Match Statistics table
CREATE TABLE IF NOT EXISTS match_statistic (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES player(id),
    match_date DATE NOT NULL,
    minutes_played INTEGER NOT NULL,
    points_scored INTEGER NOT NULL,
    rebounds INTEGER NOT NULL,
    assists INTEGER NOT NULL
);
