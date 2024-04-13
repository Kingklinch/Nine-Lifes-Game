import sqlite3
import json

from .base_model import AbstractBaseModel
from .constants import PATH_TO_DB
from .question import Question

class GameQuestion(AbstractBaseModel):
    TABLE_NAME = "gamequestions"

    def __init__(self, id=None, game_id=None, question_id=None, is_answered_correctly=None) -> None:
        self.id = id
        self.game_id = game_id
        self.question_id = question_id
        self.is_answered_correctly = is_answered_correctly

    def save(self):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()

            if self.id:
                query = f"UPDATE {self.TABLE_NAME} SET game_id=?, question_id=?, is_answered_correctly=? WHERE id=?"
                cursor.execute(
                    query,
                    (self.game_id, self.question_id, self.is_answered_correctly, self.id)
                )
            else:
                query = f"INSERT INTO {self.TABLE_NAME} (game_id, question_id, is_answered_correctly) VALUES (?, ?, ?)"
                cursor.execute(
                    query, 
                    (self.game_id, self.question_id, self.is_answered_correctly)
                )
                self.id = cursor.lastrowid

    @classmethod
    def read(cls, id=None, game_id=None, question_id=None):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()

            if id:
                result = cursor.execute(f"SELECT id, game_id, question_id, is_answered_correctly FROM {cls.TABLE_NAME} WHERE id=?", (id, )).fetchone()
                return cls(id=result[0], game_id=result[1], question_id=result[2], is_answered_correctly=result[3])
            elif game_id and question_id:
                result = cursor.execute(f"SELECT id, game_id, question_id, is_answered_correctly FROM {cls.TABLE_NAME} WHERE game_id=? AND question_id=?", (game_id, question_id)).fetchone()
                if result:
                    return cls(id=result[0], game_id=result[1], question_id=result[2], is_answered_correctly=result[3])
                else:
                    return None
            else:
                results = cursor.execute(f"SELECT id, game_id, question_id, is_answered_correctly FROM {cls.TABLE_NAME}").fetchall()
                game_questions = []
                for result in results:
                    game_question = cls(id=result[0], game_id=result[1], question_id=result[2], is_answered_correctly=result[3])
                    game_questions.append(game_question)
                return game_questions

    def toJSON(self):
        return {
            "id": self.id,
            "game_id": self.game_id,
            "question_id": self.question_id,
            "is_answered_correctly": self.is_answered_correctly
        }