# utf-8
import os
import sqlite3
from flask import request, Flask, render_template, url_for, redirect, flash, g
# from flask_login import LoginManager, login_user, login_required
# from werkzeug.security import generate_password_hash, check_password_hash


from diff_script.create_test import createTest


# конфигурация
DATABASE = '/tmp/pr_ot.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'


app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, '../pr_ot.db')))


# login_manager = LoginManager(app)
# login_manager.login_view = 'index'
# login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
# login_manager.login_message_category = "success"


# @login_manager.user_loader
# def load_user(user_id):
#     # print('load_user_', user_id )
#     return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# def create_db():
#     """Вспомогательная функция для создания таблиц БД"""
#     db = connect_db()
#     with app.open_resource('sq_db.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#     db.close()

def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None
@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = createTest()


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/', methods=['POST'])
@app.route('/create_test', methods=['POST'])
def create_test():
    if request.method == 'POST':
        qestion = request.form['qestion']
        answers = request.list_storage_class
        #  проверки в базе
        if not qestion:
            flash('ОШИБКА, проверьте вопрос!')
            return redirect(url_for('create_test'))
        if not answers:
            flash('ОШИБКА, проверьте ответы!')
            return redirect(url_for('create_test'))
        label, qestion, l_answer = dbase.create_qestion
        dbase.past_data(label, qestion, l_answer)
    return render_template('index.html')