import os
import sqlite3

PATH_TO_DB = os.path.join(
    os.path.dirname(file),
    "nine_lives_game.sqlite"
)

create_categories_table_query = """
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
"""

create_difficulty_levels_table_query = """
CREATE TABLE difficulty_levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
"""

create_questions_table_query = """
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT,
    answer_text TEXT,
    category_id INTEGER,
    difficulty_id INTEGER,
    points INTEGER,
    FOREIGN KEY(category_id) REFERENCES categories(id),
    FOREIGN KEY(difficulty_id) REFERENCES difficulty_levels(id)
)
"""

create_users_table_query = """
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    playername TEXT,
    email TEXT,
    password_hash TEXT
)
"""

create_games_table_query = """
CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    score INTEGER,
    remaining_lives INTEGER,
    start_time TEXT,
    end_time TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
"""

create_gamequestions_table_query = """
CREATE TABLE gamequestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    question_id INTEGER,
    is_answered_correctly BOOLEAN,
    FOREIGN KEY(game_id) REFERENCES games(id),
    FOREIGN KEY(question_id) REFERENCES questions(id)
)
"""

create_highscores_table_query = """
CREATE TABLE highscores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    score INTEGER,
    timestamp TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
"""

create_powerups_table_query = """
CREATE TABLE powerups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    cost INTEGER
)
"""

create_playerpowerups_table_query = """
CREATE TABLE playerpowerups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER,
    powerup_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(player_id) REFERENCES players(id),
    FOREIGN KEY(powerup_id) REFERENCES powerups(id)
)
"""

with sqlite3.connect(PATH_TO_DB) as connection:
    cursor = connection.cursor()

    for query in [
        create_categories_table_query,
        create_difficulty_levels_table_query,
        create_questions_table_query,
        create_players_table_query,
        create_games_table_query,
        create_gamequestions_table_query,
        create_highscores_table_query,
        create_powerups_table_query,
        create_playerpowerups_table_query
    ]:
        cursor.execute(query)