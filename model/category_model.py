import sqlite3
import json

from .base_model import AbstractBaseModel
from .constants import PATH_TO_DB

class Category(AbstractBaseModel):
    TABLE_NAME = "categories"

    def __init__(self, id=None, name=None) -> None:
        self.id = id
        self.name = name

    def save(self):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()

            if self.id:
                query = f"UPDATE {self.TABLE_NAME} SET name=? WHERE id=?"
                cursor.execute(
                    query,
                    (self.name, self.id)
                )
            else:
                query = f"INSERT INTO {self.TABLE_NAME} (name) VALUES (?)"
                cursor.execute(
                    query, 
                    (self.name,)
                )
                self.id = cursor.lastrowid

    @classmethod
    def read(cls, id=None, name=None):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()

            if id:
                result = cursor.execute(f"SELECT id, name FROM {cls.TABLE_NAME} WHERE id=?", (id, )).fetchone()
                return cls(id=result[0], name=result[1])
            elif name:
                result = cursor.execute(f"SELECT id, name FROM {cls.TABLE_NAME} WHERE name=?", (name, )).fetchone()
                return cls(id=result[0], name=result[1])
            else:
                results = cursor.execute(f"SELECT id, name FROM {cls.TABLE_NAME}").fetchall()
                categories = []
                for result in results:
                    category = cls(id=result[0], name=result[1])
                    categories.append(category)
                return categories

    def toJSON(self):
        return {
            "id": self.id,
            "name": self.name
        }