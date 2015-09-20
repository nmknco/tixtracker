DROP TABLE IF EXISTS events;
CREATE TABLE events (
    eventId BIGINT PRIMARY KEY,
    venueId BIGINT,
    homeTeam VARCHAR(31),
    awayTeam VARCHAR(31),
    hometeamId BIGINT,
    dateLocal VARCHAR(31),
    dateUTC VARCHAR(31),
    title VARCHAR(255),
    url TEXT,
    FOREIGN KEY (venueId) REFERENCES venues(venueId)
);