# Модуль для чтения  вопросов из БД
import random
import sqlite3


class readTest():
    def __init__(self):
        self.name_test = None
        self.qestion = None
        self.answer = ''
        self.answer_just = None
        self.path = None
        self.label = None
        self.rez_dict = {}
        self.n_qestion = 5
        self.list_answer_just = []
        # конфигурация
        self.DATABASE = 'pr_ot.db'
        self.DEBUG = True
        self.SECRET_KEY = 'fdgfh78@#5?>g5864y56wfewe2342'


    # def read_list_just(self):
    #     try:
    #         self.__cur.execute(f"SELECT a_just FROM tests")
    #         res = self.__cur.fetchall()
    #         j_res = dict(res)['a_just']
    #         if not res:
    #             print("НЕТ ДАННЫХ")
    #             return False
    #         return res
    #     except sqlite3.Error as e:
    #         print("Ошибка получения данных из БД(read_list_just) " + str(e))


    def read_test(self, path):
        try:
            connection = sqlite3.connect(path)
            list_label = []
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute(f'SELECT label from tests')
            result = cursor.fetchall()

            for res in result:
                label_res = dict(res)['label']
                list_label.append(label_res)

            # Создание случайного набора вопросов c ответами
            list_label_use = []
            for i in range(self.n_qestion):
                self.rnd_label = random.choice(list_label)
                cursor.execute(f"SELECT qestion, answer FROM tests WHERE label = {self.rnd_label}")
                res = cursor.fetchone()
                q_res = dict(res)['qestion']
                a_res = dict(res)['answer']
                self.rez_dict[self.rnd_label] = {q_res: a_res}
                list_label_use.append(self.rnd_label)

                # Список правильных ответов
                cursor.execute(f"SELECT a_just FROM tests WHERE label = {self.rnd_label}")
                res = cursor.fetchone()
                j_res = dict(res)['a_just']
                self.list_answer_just.append(j_res)
                list_label.remove(self.rnd_label)
            connection.commit()
            connection.close()

        except sqlite3.Error as e:
            print("Ошибка получения вопросов из БД(read_test) " + str(e))
        return self.rez_dict, self.list_answer_just, list_label_use



