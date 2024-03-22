import sqlite3

from base_model import AbstractBaseModel
from quizDBsetup import populate_tables


class Game(AbstractBaseModel):
    def __init__(self, nb_of_players=None, date=None):
        self.nb_players = nb_of_players,
        self.date = date

    def create(self):
        query = "INSERT INTO Game (nb_of_players, date) VALUES (?,?);"
        with sqlite3.connect("NLG") as connection:
            cursor = connection.cursor()
            cursor.execute(query, (self.nb_players, self.date))

    def read(self):
        query = "SELECT * FROM Game;"
        with sqlite3.connect("NLG") as connection:
            cursor = connection.cursor()
            results = cursor.execute(query).fetchall()
            display = []
        for result in results:
            game = Game(nb_of_players=result[1], date=result[2])
            display.append(game)

        return display

    def readById(self, i=None):
        query = "SELECT * FROM Game WHERE date=?;"
        with sqlite3.connect("NLG") as connection:
            cursor = connection.cursor()
            result = cursor.execute(query, self.date).fetchone()

        return result

    def update(self, i=None):
        if i is not None:
            query = "UPDATE Game SET nb_of_players=?, date=? WHERE id_game=?;"
            with sqlite3.connect("NLG") as connection:
                cursor = connection.cursor()
                cursor.execute(query, (self.nb_players, self.date, i))
            return
        return "No Id for the update"

    def deleteById(self, i=None):
        query = "DELETE FROM Game WHERE date=?;;"
        with sqlite3.connect("NLG") as connection:
            cursor = connection.cursor()
            cursor.execute(query, self.date)

    def delete(self):
        query = "DELETE FROM Game;"
        with sqlite3.connect("NLG") as connection:
            cursor = connection.cursor()
            cursor.execute(query)

class QuestionManager:
    def __init__(self, connection):
    with sqlite3.connect("NLG") as connection:

    def get_questions_category_and_difficulty(self, Category, DifficultyLevels):
        cursor = self.connection.cursor()
        cursor.execute(
            '''SELECT question, option1, option2, option3, option4, correct_answer FROM Quiz
            JOIN Category ON Quiz.id_category = Category.id_category
            JOIN DifficultyLevels ON Quiz.id_difficulty = DifficultyLevels.id_difficulty
            WHERE Category.name = ? AND DifficultyLevels.name ?''', (Category, DifficultyLevels)
        )

    return questions

    questions = get_questions_category_and_difficulty('History', 'Easy')
    for question in questions:
         question, option1, option2, option3, option4, correct_answer = question
         print("Question", question)
         print("Options")
         print("1. ", option1)
         print("1. ", option2)
         print("1. ", option3)
         print("1. ", option4)
         print("Answer:", correct_answer)
         print()

class InsertQuestions:
    def init(self, database):
        self.database = database

    def insert_question(self, category_id, difficulty_id, question, option1, option2, option3, option4, correct_answer):
        with sqlite3.connect("NLG") as connection:
        cursor = connection.cursor()
        cursor.execute(
            '''
            INSERT INTO Questions (id_category, id_difficulty, question, option1, option2, option3, option4, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (id_category, id_difficulty, question, option1, option2, option3, option4, correct_answer)
        )
inserter = insert_question('Quiz')
inserter.insert_question(1, 1, "What year did World War II end?", "1942", "1944", "1945", "1950", 3)
        

        questions = cursor.fetchall()
            cursor.close()

connection.commit()
cursor.close
connection.close

