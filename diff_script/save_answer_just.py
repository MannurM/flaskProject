#  Модуль записи списка правильных ответов в БД

import sqlite3
from sqlite3 import Error

class SaveAnswer():
    def __init__(self):
        self.id = None
        self.list_answer_just = None

        # конфигурация
        self.DATABASE = 'pr_ot.db'
        self.DEBUG = True
        self.SECRET_KEY = 'fdgfh78@#5?>g5864y56wfewe2342'

    def connect_db(self):
        conn = sqlite3.connect(self.DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    def create_connection(self):
        connection = None
        try:
            connection = sqlite3.connect('../pr_ot.db')
            cur = connection.cursor()
            print("Connection to SQLite DB successful")
            cur.execute('CREATE TABLE IF NOT EXISTS a_just (id integer, laj blob, llu blob)')
            connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    def save_(self, user_id, list_answer_just, list_label_use):
        try:
            laj = str(list_answer_just)
            llu = str(list_label_use)
            connection = sqlite3.connect('../pr_ot.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO a_just (id, laj, llu) VALUES(?, ?, ?)", (user_id, laj, llu))
            connection.commit()
        except sqlite3.Error as e:
            print("Ошибка записи данных в БД(save_list_just) " + str(e))
        return
