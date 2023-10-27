DROP TABLE IF EXISTS flashcards;

CREATE TABLE flashcards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    -- created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    term TEXT NOT NULL,
    defenition TEXT NOT NULL -- is definition a keyword?
);

ALTER TABLE flashcards
RENAME COLUMN defenition TO definition;

