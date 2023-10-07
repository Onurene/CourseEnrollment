PRAGMA foreign_keys = ON;
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
INSERT INTO professors (id, first_name, last_name, email, phone)
VALUES (
        1,
        'John',
        'Doe',
        'john.doe@gmail.com',
        4155551234
    ),
    (
        2,
        'Mary',
        'Smith',
        'mary.smith@yahoo.com',
        4155555678
    ),
    (
        3,
        'David',
        'Johnson',
        'david.johnson@outlook.com',
        4155558765
    ),
    (
        4,
        'Sarah',
        'Williams',
        'sarah.williams@email.com',
        4155554321
    ),
    (
        5,
        'Michael',
        'Brown',
        'michael.brown@hotmail.com',
        4155557890
    ),
    (
        6,
        'Jennifer',
        'Taylor',
        'jennifer.taylor@email.com',
        4155556543
    ),
    (
        7,
        'Brian',
        'Anderson',
        'brian.anderson@gmail.com',
        4155559876
    ),
    (
        8,
        'Laura',
        'Clark',
        'laura.clark@yahoo.com',
        4155552109
    ),
    (
        9,
        'Matthew',
        'Young',
        'matthew.young@email.com',
        4155558762
    ),
    (
        10,
        'Karen',
        'Hall',
        'karen.hall@hotmail.com',
        4155555555
    );
COMMIT;