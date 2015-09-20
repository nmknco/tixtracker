DROP TABLE IF EXISTS venues;
CREATE TABLE venues (
    venueId BIGINT PRIMARY KEY,
    address VARCHAR(63),
    name VARCHAR(63),
    city VARCHAR(31),
    state VARCHAR(7),
    zipCode VARCHAR(15),
    country VARCHAR(7),
    latitude DECIMAL(15,7),
    longitude DECIMAL(15,7),
    timezone VARCHAR(7),
    url TEXT
);