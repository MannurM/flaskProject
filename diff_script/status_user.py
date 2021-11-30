# вызов статуса пользователя, сохранение статуса пользователя
import sqlite3
from project_web_Flask_2 import dbase



class StatusUser():
    def __init__(self):
        self.theme, self.edu_materials, self.exsersis, self.exzamen = None, None, None, None
        self.name, self.firstname, self.lastname = None, None, None
        self.status, self.count_prob, self.rez_procent = None, None, None


    def status_user(self, user_id=None):
        self.theme, self.edu_materials, self.exsersis, self.exzamen = dbase.getCourse()
        self.name, self.firstname, self.lastname, self.status, self.count_prob, self.rez_procent = dbase.getStatus(user_id=user_id)
        data = {
            'theme': self.theme,
            'edu_materials': self.edu_materials,
            'exsersis': self.exsersis,
            'exzamen': self.exzamen,
            'status': self.status,
            'count_prob': self.count_prob,
            'name': self.name,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'user_id': user_id,
            'rez_procent': self.rez_procent,
            }
        return data

    def save_status_user(self, user_id=None, path=None, data=None):
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        status_course = data['status']
        count_prob = data['count_prob']
        rez_procent = data['rez_procent']
        id = data['user_id']
        update_date = (status_course, count_prob, rez_procent, id)
        cursor.execute("UPDATE users SET status_course = ?, count_prob = ?, rez_procent = ? WHERE id = ?", update_date)
        # cursor.execute("UPDATE users  SET  = rez_procent WHERE id = id")
        connection.commit()
        connection.close()

if __name__ == '__main__':
    su = StatusUser()
    path = '../pr_ot.db'
    res =su.status_user(path)
    print(res)

