DROP TABLE IF EXISTS genes;

CREATE TABLE genes (
    chromosome TEXT NOT NULL,
    start INTEGER,
    end INTEGER,
    strand TEXT NOT NULL,
    protein_name TEXT NOT NULL,
    sequence TEXT NOT NULL
);


