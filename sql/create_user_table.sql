DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    pword TEXT NOT NULL,
    salt TEXT NOT NULL,
    deleted BOOLEAN DEFAULT FALSE,
    location_name TEXT,
    latitute REAL,
    longitude REAL
);