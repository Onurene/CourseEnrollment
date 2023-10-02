PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS professors;
CREATE TABLE professors (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone INTEGER NOT NULL
);
-- values generated using chatGPT
INSERT INTO professors (id, first_name, last_name, email, phone) VALUES (1, 'John', 'Doe', 'john.doe@gmail.com', 4155551234);
INSERT INTO professors (id, first_name, last_name, email, phone) VALUES (2, 'Mary', 'Smith', 'mary.smith@yahoo.com', 4155555678);
INSERT INTO professors (id, first_name, last_name, email, phone) VALUES (3, 'David', 'Johnson', 'david.johnson@outlook.com', 4155558765);
INSERT INTO professors (id, first_name, last_name, email, phone) VALUES (4, 'Sarah', 'Williams', 'sarah.williams@email.com', 4155554321);
INSERT INTO professors (id, first_name, last_name, email, phone) VALUES (5, 'Michael', 'Brown', 'michael.brown@hotmail.com', 4155557890);
INSERT INTO professors (id, first_name, last_name, email, phone) VALUES (6, 'Jennifer', 'Taylor', 'jennifer.taylor@email.com', 4155556543);
INSERT INTO professors (id, first_name, last_name, email, phone) VALUES (7, 'Brian', 'Anderson', 'brian.anderson@gmail.com', 4155559876);
INSERT INTO professors (id, first_name, last_name, email, phone) VALUES (8, 'Laura', 'Clark', 'laura.clark@yahoo.com', 4155552109);
INSERT INTO professors (id, first_name, last_name, email, phone) VALUES (9, 'Matthew', 'Young', 'matthew.young@email.com', 4155558762);
INSERT INTO professors (id, first_name, last_name, email, phone) VALUES (10, 'Karen', 'Hall', 'karen.hall@hotmail.com', 4155555555);
COMMIT;
