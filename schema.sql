DROP TABLE IF EXISTS datapoints;


CREATE TABLE datapoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hours_studied REAL NOT NULL,
    sleep_hours REAL NOT NULL,
    performance_level INTEGER NOT NULL
);
