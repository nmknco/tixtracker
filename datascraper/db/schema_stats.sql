DROP TABLE IF EXISTS stats;
CREATE TABLE stats (
    eventId BIGINT,
    recordTime DATETIME,
    zoneId BIGINT,
    zoneName VARCHAR(63),
    numOfLis INT,
    numOfTix INT,
    lowPrice DECIMAL(10,2),
    FOREIGN KEY (eventId) REFERENCES venues(venueId)
);