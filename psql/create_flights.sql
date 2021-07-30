CREATE TABLE IF NOT EXISTS flights (
    "id"                      INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL UNIQUE,
    "src_iata"                VARCHAR NOT NULL,
    "dest_iata"               VARCHAR NOT NULL,
    "departureDate"           TIMESTAMP NOT NULL,
    "departureNumOfTransfers" INTEGER NOT NULL,
    "duration"                VARCHAR NOT NULL,
    "returnDate"              TIMESTAMP NOT NULL,
    "returnNumOfTransfers"    INTEGER NOT NULL,
    "lastTicketingDate"       DATE NOT NULL,
    "numOfavSeats"            INTEGER NOT NULL,
    "numOfAdults"             INTEGER NOT NULL,
    "currency"                VARCHAR NOT NULL,
    "total"                   FLOAT NOT NULL
);
