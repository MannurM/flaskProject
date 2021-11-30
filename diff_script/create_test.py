# модуль для создания тестов. Запись вопросов и ответов в БД

# вопрос, варианты ответа правильный ответ

import os, random
import sqlite3
from sqlite3 import Error


class createTest():
    def __init__(self):
        self.name_test = None
        self.qestion = None
        self.answer = ''
        self.answer_just = None
        self.path = None
        self.label = None
        # конфигурация
        self.DATABASE = 'pr_ot.db'
        self.DEBUG = True
        self.SECRET_KEY = 'fdgfh78@#5?>g5864y56wfewe2342'

    def connect_db(self):
        conn = sqlite3.connect(self.DATABASE)
        conn.row_factory = sqlite3.Row
        return conn

    def create_db(self):
        db = self.connect_db()
        with open('../sq_db.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
        db.close()

    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            cur = connection.cursor()
            print("Connection to SQLite DB successful")
            cur.execute('CREATE TABLE IF NOT EXISTS tests (label integer, qestion text, answer blob, a_just blob)')
            connection.commit()
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection


    def past_data(self, path, label, qestion, l_answer, a_just):
        l_answer=str(l_answer)
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        print(label, qestion, l_answer, a_just)
        cursor.execute("INSERT INTO tests VALUES(?, ?, ?, ? )", (label, qestion, l_answer, a_just))
        connection.commit()


    def create_qestion(self):
        print('Введите вопрос в поле')
        self.qestion = input()
        self.label = random.randint(0, 10000)
        # TODO сделать проверку случайных чисел на наличие в БД
        # while self.label is self.label_set:
        #     self.label_set.add(self.label)
        #     if len(self.label_set) >= 10000:
        #         break
        #     self.label = random.randint(0, 10000)
        self.l_answer, self.answer_just = self.create_answer(self.label)
        return self.label, self.qestion, self.l_answer, self.answer_just


    def create_answer(self, label):
        self.label = label
        print('Введите ответы!')
        print('Сколько будет ответов? введите число ответов')
        self.sum_answer = input()
        # проверить на число
        while not self.sum_answer.isdigit() or self.sum_answer < '1':
            print('Вы ввели  неверно!')
            print('Введите число 1 или 2, ...')
            self.sum_answer = input()
        self.sum_answer = int(self.sum_answer)
        self.list_answer=[]
        for i in range(self.sum_answer):
            print(f'введите {i + 1} ответ:')
            self.answer = input()
            print(f'это верный вариант?? 1-да, любой другой символ - нет')
            self.ans_just = input()
            if self.ans_just == '1':
                self.ans_just = '1'
                self.answer_just = self.answer
            else:
                self.ans_just = '0'
            self.full_answer = self.answer
            self.list_answer.append(self.full_answer)
        return self.list_answer, self.answer_just


if __name__ == '__main__':
    ct = createTest()
    ct.create_db()

    otv = True
    while otv:
        path = "C:/Users/ZMan/PycharmProjects/flaskProject/pr_ot.db"
        ct.create_connection(path)
        label, qestion, l_answer, answer_just = ct.create_qestion()
        ct.past_data(path, label, qestion, l_answer, answer_just)
        print(" ЕЩЕ вопрос 1-да")
        vopr = input()
        if vopr == '1':
            otv = True
        else:
            otv = False


# TODO упорядочить работу модуля
# TODO создать функцию для импорта фопросов и ответо из csv
# TODO упростить запись вопросов в ответ--> убрать номер вопроса, признак правильности вопроса добавить к ответу