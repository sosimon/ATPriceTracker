CREATE TABLE Price(
    id SERIAL PRIMARY KEY,
    listingId INTEGER,
    make VARCHAR(50),
    model VARCHAR(50),
    year INTEGER,
    mileage INTEGER,
    color VARCHAR(50),
    price INTEGER,
    createDate TIMESTAMP NOT NULL
);
