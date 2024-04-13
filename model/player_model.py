import sqlite3
import json

from .base_model import AbstractBaseModel
from .constants import PATH_TO_DB
from .files import File
from .subjects import Subject

class Player(AbstractBaseModel):
    TABLE_NAME = "players"

    def __init__(self, id=None, username=None, email=None, password=None) -> None:
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()

            if self.id:
                query = f"UPDATE {self.TABLE_NAME} SET username=?, email=?, password=? WHERE id=?"
                cursor.execute(
                    query,
                    (self.username, self.email, self.password, self.id)
                )
            else:
                query = f"INSERT INTO {self.TABLE_NAME} (username, email, password) VALUES (?,?,?)"
                cursor.execute(
                    query, 
                    (self.username, self.email, self.password)
                )
                self.id = cursor.lastrowid

    @classmethod
    def read(cls, id=None, username=None, email=None):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()

            if id:
                result = cursor.execute(f"SELECT id, username, email, password FROM {cls.TABLE_NAME} WHERE id=?", (id, )).fetchone()
                return cls(id=result[0], username=result[1], email=result[2], password=result[3])
            elif username:
                result = cursor.execute(f"SELECT id, username, email, password FROM {cls.TABLE_NAME} WHERE username=?", (username, )).fetchone()
                return cls(id=result[0], username=result[1], email=result[2], password=result[3])
            elif email:
                result = cursor.execute(f"SELECT id, username, email, password FROM {cls.TABLE_NAME} WHERE email=?", (email, )).fetchone()
                return cls(id=result[0], username=result[1], email=result[2], password=result[3])
            else:
                results = cursor.execute(f"SELECT id, username, email, password FROM {cls.TABLE_NAME}").fetchall()
                players = []
                for result in results:
                    player = cls(id=result[0], username=result[1], email=result[2], password=result[3])
                    players.append(player)
                return players

    def delete(self):
        with sqlite3.connect(PATH_TO_DB) as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {self.TABLE_NAME} WHERE id=?", (self.id,))
        self.id = None

    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }