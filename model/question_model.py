import sqlite3
import json

from .base_model import AbstractBaseModel
from .constants import PATH_TO_DB
from .category import Category
from .difficulty_level import DifficultyLevel

class Question(AbstractBaseModel):
    TABLE_NAME = "questions"

    def __init__(self, id=None, question_text=None, answer_text=None, category_id=None, difficulty_id=None, points=None) -> None:
        self.id = id
        self.question_text = question_text
        self.answer_text = answer_text
        self.category_id = category_id
        self.difficulty_id = difficulty_id
        self.points = points

    def save(self):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()

            if self.id:
                query = f"UPDATE {self.TABLE_NAME} SET question_text=?, answer_text=?, category_id=?, difficulty_id=?, points=? WHERE id=?"
                cursor.execute(
                    query,
                    (self.question_text, self.answer_text, self.category_id, self.difficulty_id, self.points, self.id)
                )
            else:
                query = f"INSERT INTO {self.TABLE_NAME} (question_text, answer_text, category_id, difficulty_id, points) VALUES (?, ?, ?, ?, ?)"
                cursor.execute(
                    query, 
                    (self.question_text, self.answer_text, self.category_id, self.difficulty_id, self.points)
                )
                self.id = cursor.lastrowid

    @classmethod
    def read(cls, id=None, category_id=None, difficulty_id=None):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()

            if id:
                result = cursor.execute(f"SELECT id, question_text, answer_text, category_id, difficulty_id, points FROM {cls.TABLE_NAME} WHERE id=?", (id, )).fetchone()
                return cls(id=result[0], question_text=result[1], answer_text=result[2], category_id=result[3], difficulty_id=result[4], points=result[5])
            elif category_id and difficulty_id:
                results = cursor.execute(f"SELECT id, question_text, answer_text, category_id, difficulty_id, points FROM {cls.TABLE_NAME} WHERE category_id=? AND difficulty_id=?", (category_id, difficulty_id)).fetchall()
                questions = []
                for result in results:
                    question = cls(id=result[0], question_text=result[1], answer_text=result[2], category_id=result[3], difficulty_id=result[4], points=result[5])
                    questions.append(question)
                return questions
            else:
                results = cursor.execute(f"SELECT id, question_text, answer_text, category_id, difficulty_id, points FROM {cls.TABLE_NAME}").fetchall()
                questions = []
                for result in results:
                    question = cls(id=result[0], question_text=result[1], answer_text=result[2], category_id=result[3], difficulty_id=result[4], points=result[5])
                    questions.append(question)
                return questions

    def toJSON(self):
        return {
            "id": self.id,
            "question_text": self.question_text,
            "answer_text": self.answer_text,
            "category_id": self.category_id,
            "difficulty_id": self.difficulty_id,
            "points": self.points
        }