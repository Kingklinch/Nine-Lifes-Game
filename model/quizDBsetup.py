import sqlite3

def populate_tables(cursor):
    cursor.executemany(
        '''INSERT INTO Category (id_category, name) VALUES (?, ?)''',
        [
            (1, 'History'),
            (2, 'Geography'),
            (3, 'Sport'),
            (4, 'Entertainment')
        ]
    )
     cursor.executemany(
        '''INSERT INTO DifficultyLevels (id_difficulty, name) VALUES (?, ?)''',
        [
            (1, 'Easy'),
            (2, 'Medium'),
            (3, 'Hard'),
            (4, 'Mastrer')
        ]
    )