import sqlite3
import random
import datetime


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
        self.name_test = None
        self.qestion = None
        self.answer = ''
        self.answer_just = None
        self.path = None
        self.label = None
        self.rez_dict = {}
        self.n_qestion = 5
        self.list_answer_just = []


    def getCourse(self):
        try:
            self.__cur.execute(f"SELECT id_course, theme, edu_materials, edu_other, edu_additional FROM courses")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения курса из БД " + str(e))
        return False

    def read_for_sert(self):
        try:
            self.__cur.execute(f"SELECT theme, course_hourses FROM courses")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения курса из БД " + str(e))
        return False



    def getStatus_name(self, user_id):
        try:
            user_id = user_id
            self.__cur.execute("SELECT name, firstname, lastname FROM users WHERE id = ? LIMIT 1", user_id)
            res = self.__cur.fetchone()
            if res:
                print('res_true', res)
                return res
            print('res_false',res)
        except sqlite3.Error as e:
            print("Ошибка получения статуса имени " + str(e))
        return False


    def getStatus_exzam(self, user_id):
        try:
            user_id = user_id
            # sd = f"Select count_prob, status_exzam from exzam_rezult where id={user_id}"
            # self.__cur.execute(sd, user_id)

            self.__cur.execute(f"SELECT count_prob, status_exzam, data_exzam FROM exzam_rezult WHERE id={user_id}")
            res = self.__cur.fetchone()
            if res:
                return res
            else:
                count_prob = 0
                status_exzam = 'Не сдано'
                date_exzam = 0
                return count_prob, status_exzam, date_exzam
        except sqlite3.Error as e:
            print("Ошибка получения статуса экзамена " + str(e))
        return False

    def insertStatus_exzam(self, user_id):
        try:
            user_id = user_id
            count_prob = 0
            status_exzam = 'Не сдано'
            date_exzam = datetime.datetime.now()
            date_exzam = date_exzam.strftime('%d-%m-%Y %H:%M:%S')
            values = (user_id, count_prob, status_exzam, date_exzam)
            self.__cur.execute("INSERT OR IGNORE INTO exzam_rezult VALUES(?, ?, ?, ?)", values)
        except sqlite3.Error as e:
            print("Ошибка записи начального статуса экзамена " + str(e))
        return

    def getProfile(self, user_id):
        try:
            select_data = ('name', 'firstname', 'lastname', 'dateborn', 'name_organization', 'position', 'email')
            self.__cur.execute(f"SELECT name, firstname, lastname, dateborn, name_suborganization, position, email FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения данных профиля" + str(e))
        return False

    def getCourseEdu(self, id_course):
        try:
            self.__cur.execute(f"SELECT edu_materials, edu_other, edu_additional FROM courses WHERE id_course={id_course}")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения курса из БД(getCourseEdu) " + str(e))
        return

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден!")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(getUser) " + str(e))
        return False

    def read_organization(self):
        try:
            self.__cur.execute("SELECT * FROM organization_com")
            res = self.__cur.fetchone()
            if not res:
                print("Организация не найдена!")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(organization) " + str(e))
        return

    def save_protocol_N(self, data):
        try:
            protocol_N = data['protocol_N']
            number_sert = data['number_sert']
            up_date = (protocol_N, number_sert)
            self.__cur.execute("UPDATE organization_com SET protokol_N=?, number_sert=?", up_date)
        except sqlite3.Error as e:
            print("Ошибка записи данных в БД(protokol_N) " + str(e))

    def save_sertificat(self, user_id, data):
        try:
            theme = data['theme']
            protocol_N = data['protocol_N']
            number_sert = data['number_sert']
            up_date = (user_id, theme, protocol_N, number_sert)
            self.__cur.execute("INSERT INTO docs VALUES (?,?,?,?)", up_date)
        except sqlite3.Error as e:
            print("Ошибка записи данных в БД(save_sertificat) " + str(e))


    def read_sertificat(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM docs WHERE id = {user_id}")
            res = self.__cur.fetchone()
            if not res:
                print("Ошибка нет данных в БД")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(read_sertificat) " + str(e)
        return


    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден!")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(getUserByEmail) " + str(e))
        return False

    def getUserByName(self, name):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE name = '{name}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден!")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(getUserByName) " + str(e))
        return False


    def read_list_just(self, user_id):
        try:
            self.__cur.execute(f"SELECT laj, llu FROM a_just WHERE id = {user_id} ")
            res = self.__cur.fetchall()
            if not res:
                print("Нет списка правильных ответов!")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(read_list_just) " + str(e))


    def save_status_user(self, user_id, data):  # обновление статуса в БД
        status_course = data['status']
        count_prob = data['count_prob']
        date_exzam = datetime.datetime.now()
        date_exzam = date_exzam.strftime('%d-%m-%Y %H:%M:%S')
        up_date = (status_course, count_prob, date_exzam)
        self.__cur.execute(f"UPDATE exzam_rezult SET status_exzam=?, count_prob=?, data_exzam=? WHERE id = {user_id}", up_date)
        return

    def read_count_prob(self, user_id):
        try:
            print('read_count_prob')
            self.__cur.execute(f"SELECT count_prob FROM exzam_rezult WHERE id = {user_id}")
            res = self.__cur.fetchone()
            if not res:
                print("Ошибка нет данных в БД")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(read_count_prob) " + str(e))

    def save_count_prob(self, user_id, data):  # обновление результатов экзамена в БД
        count_prob = data['count_prob']
        id = data['user_id']
        up_date = (count_prob, id)
        self.__cur.execute(f"UPDATE exzam_rezult SET count_prob = ? WHERE id = {id}", up_date)
        return

    def update_profile(self, user_id, profile_data):
        self.profile_data = profile_data
        name = self.profile_data['name']
        firstname = self.profile_data['firstname']
        lastname = self.profile_data['lastname']
        dateborn = self.profile_data['dateborn']
        name_suborganization = self.profile_data['name_suborganization']
        position = self.profile_data['position']
        email = self.profile_data['email']
        user_id = user_id
        up_date = (name, firstname, lastname, dateborn, name_suborganization, position, email, user_id)
        print('update_profile', up_date)
        try:
            sqlite_update = ('Update users set name=?, firstname=?, lastname=?, dateborn=?, name_suborganization=?,\n'
                             '            position=?, email=? where id = ?')
            self.__cur.execute(sqlite_update, up_date)
            return
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД(update_profile) " + str(e))


    def read_test(self, path):
        list_label_use = []
        list_label = []
        try:
            self.__cur.execute(f'SELECT label from tests')
            result = self.__cur.fetchall()
            for res in result:
                label_res = dict(res)['label']
                list_label.append(label_res)

            # Создание случайного набора вопросов c ответами
            for i in range(self.n_qestion):
                self.rnd_label = random.choice(list_label)
                self.__cur.execute(f"SELECT qestion, answer FROM tests WHERE label = {self.rnd_label}")
                res = self.__cur.fetchone()
                q_res = dict(res)['qestion']
                a_res = dict(res)['answer']
                self.rez_dict[self.rnd_label] = {q_res: a_res}
                list_label_use.append(self.rnd_label)

                # Список правильных ответов
                self.__cur.execute(f"SELECT a_just FROM tests WHERE label = {self.rnd_label}")
                res = self.__cur.fetchone()
                j_res = dict(res)['a_just']
                self.list_answer_just.append(j_res)
                list_label.remove(self.rnd_label)

        except sqlite3.Error as e:
            print("Ошибка получения вопросов из БД(read_test) " + str(e))
        return self.rez_dict, self.list_answer_just, list_label_use

    def save_(self, user_id, list_answer_just, list_label_use):
        try:
            laj = str(list_answer_just)
            llu = str(list_label_use)
            self.__cur.execute(f"INSERT INTO a_just (id, laj, llu) VALUES(?, ?, ?)", (user_id, laj, llu))
            print('ответы записаны')
        except sqlite3.Error as e:
            print("Ошибка записи данных в БД(save_list_just) " + str(e))
        return


    # def save_list_just(self, user_id, list_answer_just):
    #     try:
    #         # TODO  сделать отдельную функцию для создания базы данных со всеми таблицами
    #         laj = str(list_answer_just)
    #         self.__cur.execute("INSERT INTO a_just (id, laj) VALUES(?, ?)", (user_id, laj))
    #     except sqlite3.Error as e:
    #         print("Ошибка записи данных в БД(save_list_just) " + str(e))