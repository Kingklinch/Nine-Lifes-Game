import sqlite3
import json

from .base_model import AbstractBaseModel
from .constants import PATH_TO_DB
from .files import File
from .subjects import Subject

class QuizGame(AbstractBaseModel):
    TABLE_NAME = "games"

    def __init__(self, id=None, player_id=None, category_id=None, difficulty_id=None, score=0, remaining_lives=9, start_time=None, end_time=None) -> None:
        self.id = id
        self.player_id = player_id
        self.category_id = category_id
        self.difficulty_id = difficulty_id
        self.score = score
        self.remaining_lives = remaining_lives
        self.start_time = start_time
        self.end_time = end_time

    def save(self):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()

            if self.id:
                query = f"UPDATE {self.TABLE_NAME} SET player_id=?, category_id=?, difficulty_id=?, score=?, remaining_lives=?, start_time=?, end_time=? WHERE id=?"
                cursor.execute(
                    query,
                    (self.player_id, self.category_id, self.difficulty_id, self.score, self.remaining_lives, self.start_time, self.end_time, self.id)
                )
            else:
                query = f"INSERT INTO {self.TABLE_NAME} (player_id, category_id, difficulty_id, score, remaining_lives, start_time, end_time) VALUES (?,?,?,?,?,?,?)"
                cursor.execute(
                    query, 
                    (self.player_id, self.category_id, self.difficulty_id, self.score, self.remaining_lives, self.start_time, self.end_time)
                )
                self.id = cursor.lastrowid

    @classmethod
    def read(cls, id=None, player_id=None):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()

            if id:
                result = cursor.execute(f"SELECT id, player_id, category_id, difficulty_id, score, remaining_lives, start_time, end_time FROM {cls.TABLE_NAME} WHERE id=?", (id, )).fetchone()
                return cls(id=result[0], player_id=result[1], category_id=result[2], difficulty_id=result[3], score=result[4], remaining_lives=result[5], start_time=result[6], end_time=result[7])
            elif player_id:
                results = cursor.execute(f"SELECT id, player_id, category_id, difficulty_id, score, remaining_lives, start_time, end_time FROM {cls.TABLE_NAME} WHERE player_id=?", (player_id, )).fetchall()
                games = []
                for result in results:
                    game = cls(id=result[0], player_id=result[1], category_id=result[2], difficulty_id=result[3], score=result[4], remaining_lives=result[5], start_time=result[6], end_time=result[7])
                    games.append(game)
                return games
            else:
                results = cursor.execute(f"SELECT id, player_id, category_id, difficulty_id, score, remaining_lives, start_time, end_time FROM {cls.TABLE_NAME}").fetchall()
                games = []
                for result in results:
                    game = cls(id=result[0], player_id=result[1], category_id=result[2], difficulty_id=result[3], score=result[4], remaining_lives=result[5], start_time=result[6], end_time=result[7])
                    games.append(game)
                return games

    def toJSON(self):
        return {
            "id": self.id,
            "player_id": self.player_id,
            "category_id": self.category_id,
            "difficulty_id": self.difficulty_id,
            "score": self.score,
            "remaining_lives": self.remaining_lives,
            "start_time": self.start_time,
            "end_time": self.end_time
        }