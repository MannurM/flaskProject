# utf-8
import io
import os
import sqlite3
import ast
import tempfile


from flask import request, Flask, render_template, url_for, redirect, flash, session, g, send_from_directory
from flask_login import LoginManager, login_user, login_required
from werkzeug.security import check_password_hash  # generate_password_hash

from FDataBase import FDataBase
from UserLogin_2 import UserLogin

# конфигурация
from creater_protokol import convert_sert, convert_protocol

DATABASE = 'pr_ot.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
data = {}
dbase = None

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'pr_ot.db')))


login_manager = LoginManager(app)
login_manager.login_view = 'index'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        name_user = request.form['name']
        user = dbase.getUserByName(name_user)
        #  проверки в базе
        if not user:
            flash('ОШИБКА, проверьте фамилию!')
        elif check_password_hash(user['hpsw'], request.form['psw']):
            userLogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False
            login_user(userLogin, remember=rm)
            user_id = UserLogin.get_id(userLogin)
            session['name'] = request.form['name']
            return redirect(url_for('courses', user_id=user_id))
        else:
            flash('ОШИБКА, проверьте фамилию и пароль')
    return render_template('index.html')


@app.route('/logout')
def logout():
    # удаляем имя пользователя из сеанса, если оно есть
    session.pop('name', None)
    return redirect(url_for('index'))


@app.route('/courses/<user_id>')
@login_required
def courses(user_id):
    data = status_user(user_id)
    return render_template('courses.html', data=data)


@app.route('/edu_mat/<user_id>')
@login_required
def edu_mat(user_id):
    db = get_db()
    dbase = FDataBase(db)
    data = status_user(user_id)
    edu_mat, edu_other, edu_additional = dbase.getCourseEdu(data['id_course'])  # TODO id_course -  будут изменяться?
    data['edu_mat'] = edu_mat  # TODO edu_other, edu_additional
    return render_template('edu_mat.html', data=data)


@app.route('/edu_test/<user_id>')
@login_required
def edu_test(user_id):
    data = status_user(user_id=user_id)
    temp_dict, list_answer_just, list_label_use = unpacking_edutest(user_id)
    # TODO вынести промежуточное сохранение результата теста? или все - таки его записывать!
    db = get_db()
    dbase = FDataBase(db)
    dbase.save_(user_id, list_answer_just, list_label_use)
    db.commit()
    global t_dict
    t_dict = temp_dict
    return render_template('edu_test.html', data=data, temp_dict=temp_dict)


@app.route('/edutest_rezult/,<user_id>', methods=['GET', 'POST'])
@login_required
def edutest_rezult(user_id):
    data = status_user(user_id=user_id)
    list_label_use, list_answer_just, data_answer = None, None, None
    if request.method == 'POST':
        data_answer = request.form.getlist('ans')
        if data_answer:
            sum_answer = len(data_answer)
            if sum_answer > 5:
                print('Ответов больше, чем нужно')  # TODO сделать вывод в приложении
            else:
                data['sum_just'], list_answer_just, data_answer, list_label_use = read_list_just(user_id, data_answer)
    data['data_answer'] = data_answer
    data['all_answer'] = list_label_use  # список номеров вопросов
    data['just_answer'] = list_answer_just
    global t_dict  # TODO не нравится глобал -  как обойти??
    return render_template('edutest_rezult.html', data=data, temp_dict=t_dict)


@app.route('/edu_exz/<user_id>')
@login_required
def edu_exz(user_id):
    data = status_user(user_id=user_id)
    temp_dict, list_answer_just, list_label_use = unpacking_edutest(user_id)
    db = get_db()
    dbase = FDataBase(db)
    dbase.save_(user_id, list_answer_just, list_label_use)
    db.commit()
    global t_dict
    t_dict = temp_dict
    return render_template('edu_exz.html', data=data, temp_dict=temp_dict)


@app.route('/eduexz_rezult/,<user_id>', methods=['GET', 'POST'])
@login_required
def eduexz_rezult(user_id):
    db = get_db()
    dbase = FDataBase(db)
    data = status_user(user_id=user_id)
    count_prob = data['count_prob']
    list_label_use, list_answer_just, data_answer = None, None, None
    if request.method == 'POST':
        data_answer = request.form.getlist('ans')
        if data_answer:
            sum_answer = len(data_answer)
            if sum_answer > 5:
                print('Ответов больше, чем нужно')
            else:
                data['sum_just'], list_answer_just, data_answer, list_label_use = read_list_just(user_id, data_answer)
    data['data_answer'] = data_answer
    data['all_answer'] = list_label_use  # список номеров вопросов
    data['just_answer'] = list_answer_just
    if data['sum_just'] >= 3:
        data['status'] = 'Сдано'
    if count_prob in [None, 0, 1, 2]:
        count_prob += 1
    else:
       data['message'] = 'Попыток больше нет!'
    data['count_prob'] = count_prob
    global t_dict  # TODO не нравится глобал -  как обойти??
    dbase.save_status_user(user_id=user_id, data=data)
    db.commit()
    return render_template('eduexz_rezult.html', data=data, temp_dict=t_dict)


@app.route('/profile/<user_id>')
@login_required
def profile(user_id):
    # TODO облагородить шаблон стилями, сделать возможность сохранить изменения в профиле в БД
    db = get_db()
    dbase = FDataBase(db)
    name, firstname, lastname, dateborn, name_suborganization, position, email = dbase.getProfile(user_id)
    data = status_user(user_id=user_id)
    profile_data = {
        'name': name,
        'firstname': firstname,
        'lastname': lastname,
        'dateborn': dateborn,
        'name_suborganization': name_suborganization,
        'position': position,
        'email': email
        }
    save_profile = {}
    if request.method == 'POST':
        save_profile['name'] = request.form['name']
        save_profile['firstname'] = request.form['firstname']
        save_profile['lastname'] = request.form['lastname']
        save_profile['dateborn'] = request.form['dateborn']
        save_profile['name_suborganization'] = request.form['name_suborganization']
        save_profile['position'] = request.form['position']
        save_profile['email'] = request.form['email']  # request.form.get('email')
        new_profile_data = check_save_profile(user_id, save_profile, profile_data)
        profile_data = dbase.updata_profile(user_id, new_profile_data)
        db.commit()
    return render_template('profile.html', data=data, profile_data=profile_data)


@app.route('/check_profile/<user_id>', methods=['GET', 'POST'])
@login_required
def check_profile(user_id):
    db = get_db()
    dbase = FDataBase(db)
    data = status_user(user_id)
    name, firstname, lastname, dateborn, name_suborganization, position, email = dbase.getProfile(user_id)
    profile_data = {
        'name': name,
        'firstname': firstname,
        'lastname': lastname,
        'dateborn': dateborn,
        'name_suborganization': name_suborganization,
        'position': position,
        'email': email
        }
    save_profile = {}
    if request.method == 'POST':
        save_profile['name'] = request.form['name']
        save_profile['firstname'] = request.form['firstname']
        save_profile['lastname'] = request.form['lastname']
        save_profile['dateborn'] = request.form['dateborn']
        save_profile['name_suborganization'] = request.form['name_suborganization']
        save_profile['position'] = request.form['position']
        save_profile['email'] = request.form['email']  # request.form.get('email')
        new_profile_data = check_save_profile(user_id, save_profile, profile_data)
        profile_data = dbase.update_profile(user_id, new_profile_data)
        db.commit()
        # TODO создать удостоверение и протокол  в docx, конвертировать в ПДФ (JPG? TIFF?)или сразу создать в ПДФ
        # TODO для организатора оставить возможность скачать удостоверения в докс
        # TODO Записать протокол и удостоверение в БД
        return redirect(url_for("sertification", user_id=user_id))
    return render_template('check_profile.html', data=data, profile_data=profile_data)


@app.route('/sertification/<user_id>')
@login_required
def sertification(user_id):
    db = get_db()
    dbase = FDataBase(db)
    theme, blob_sertificate, blob_protocol, name_protocol, name_sert = create_sert(user_id)
    # TODO переконвертировать в двоичные данные и сохранить
    #  а при распаковке??? в другой формат в ПДФ ?? и потом сохранить
    print('выполнено -  протокол и удостоверение созданы')
    dbase.save_sertificat(user_id, theme, blob_sertificate, blob_protocol, name_protocol, name_sert)
    db.commit()
    # TODO проверка записи в БД удостоверения и протокола
    return redirect(url_for('courses', user_id=user_id))


@app.route('/register')
def register():
    return render_template('templates_rich/registration.html')


@app.route("/exit")
def exit():
    session.pop('name', None)
    return render_template('exit.html')


@app.route("/save_template_docs", methods=['GET', 'POST'])
def save_template_docs():
    save = {}
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        theme, course_hourses = dbase.read_for_sert()
        if theme == request.form['theme']:
            prot = request.files['prot']
            sert = request.files['sert']
            save['theme'] = request.form['theme']
            save['prot'], save['sert'] = convert_path(prot, sert)
            dbase.create_template_sert(save)
            db.commit()
            return redirect(url_for('index'))
        else:
            flash('нет такой темы!')
    return render_template('save_template_docs.html')


# Внутренние функции
# Модуль для проверки результатов тестов
# TODO есть необходимость считать общее количество правильных ответов!!!
def check_edu_test(list_answer_just, data_answer):
    sum_just = 0
    for answer in data_answer:
        if answer in list_answer_just:
            sum_just += 1
    return sum_just


# Считывание статистики по ID
def status_user(user_id):
    db = get_db()
    dbase = FDataBase(db)
    name, firstname, lastname = dbase.getStatus_name(user_id=user_id)
    theme, count_prob, status_exzam, data_exzam = dbase.getStatus_exzam(user_id=user_id)
    id_course, theme, edu_materials, edu_other, edu_additional = dbase.getCourse()
    data = {
        'id_course': id_course,
        'theme': theme,
        'edu_materials': edu_materials,
        'edu_other': edu_other,
        'edu_additional': edu_additional,
        'status': status_exzam,
        'count_prob': count_prob,
        'name': name,
        'firstname': firstname,
        'lastname': lastname,
        'user_id': user_id,
        'sum_just': 0,
        }
    if dbase.check_exist(user_id=user_id):
        id, theme_1, protocol, sertificate, name_protocol, name_sert = dbase.read_sertificat(user_id)
        data['sert'] = 1
        # TODO data['protocol'], data['sertificate'] - это ссылки на файлы в БД
        # TODO проверка  рендерится - если скачать сертификат, то запускается скрипт
        # ToDO скрипт - Передается user_id, theme_1. Формируется запрос в БД. ОТвет конвертируется в docx.
        # TODO Ответ формируется во временной памяти. Открывается новая страница браузера с параметром download.
        # TODO Предлагается путь для сохранения.
        blob_data = protocol
        filename = name_protocol
        protocol = convert_from_binary_data(filename, blob_data)
        data['protocol'] = protocol
        blob_data = sertificate
        filename = name_sert
        sertificate = convert_from_binary_data(filename, blob_data)
        data['sertificate'] = sertificate
    return data


# Распаковка теста из БД
def unpacking_edutest(user_id):
    temp_dict = {}
    list_answer_just = []
    db = get_db()
    dbase = FDataBase(db)
    qa_dict, dict_just, list_label_use = dbase.read_test('pr_ot.db')
    for label, val in qa_dict.items():
        for qestion, answer in val.items():
            answer = ast.literal_eval(answer)  # Избавляет от кавычек список
            answer_not_resp = []
            for ans in answer:
                answer_not_resp.append(ans)  # список всех ответов
            temp_dict[qestion] = answer_not_resp  # словарь из ключа - вопроса, значений - вариантов ответов
    for value in dict_just:
        answer_just = value
        list_answer_just.append(answer_just)
    return temp_dict, list_answer_just, list_label_use


# Сравнение ответов в тесте
# TODO Разделить ответы экзаменационные и пробные!!!
def read_list_just(user_id, data_answer):
    db = get_db()
    dbase = FDataBase(db)
    list_label_just = dbase.read_list_just(user_id)
    if not list_label_just:
        print('не прочитались данные')
    list_answer_just = []
    list_label_use = []
    for i in list_label_just:
        laj = tuple(i)
        list_answer_just = laj[0]
        list_label_use = laj[1]
    sum_just = check_edu_test(list_answer_just, data_answer)  # модуль проверки формы
    # dbase.save_status_user(user_id=user_id, data=data)  # TODO записывать в БД полное изменение всех параметоров?
    return sum_just, list_answer_just, data_answer, list_label_use


def check_save_profile(user_id, save_profile, profile_data):
    for key, value in profile_data.items():
        if value == '':
            profile_data[key] = save_profile[key]
        elif value not in save_profile[key]:
            profile_data[key] = save_profile[key]
    return profile_data


def convert_from_binary_data(filename, blob_data):
    # TODO 1. передать в функцию имя файла и бинарный файл,
    # TODO 2. сразу бинарный файл и  название файла в БД (название файла удостоверения иил протокола сохранить в БД)
    # TODO 3. открыть файл с навазнием из БД, закачать бинарные данные данные , закрыть файл, вернуть файл из конвертера
    name_file = filename
    b_file = io.BytesIO(blob_data)
    # TODO при открытии файла -  файл сохраняется в корневом каталоге в нужном docx формате. как оставить его в памяти
    # TODO и перенести в к пользователю
    with open(name_file, 'wb') as file:
        name_file = file.write(blob_data)
    b_file.close()
    return name_file


def convert_path(prot, sert):
    with tempfile.TemporaryDirectory() as tmpdirname:
        prot = f'{tmpdirname}\_{prot}'
        with open(prot, 'rb') as doc:
            blob_data_prot = doc.read()
        sert = f'{tmpdirname}\_{sert}'
        with open(sert, 'rb') as doc:
            blob_data_sert = doc.read()
        return blob_data_prot, blob_data_sert


def create_sert(user_id): # вариант docx
    db = get_db()
    dbase = FDataBase(db)
    # TODO  в будущем сделать скрипты работы с БД
    name, firstname, lastname, dateborn, name_suborganization, position, email = dbase.getProfile(user_id)
    theme, count_prob, status_exzam, data_exzam = dbase.getStatus_exzam(user_id)
    theme2, course_hourses = dbase.read_for_sert()
    data_org = dbase.read_organization()
    data_sert={}
    for key in data_org.keys():
        data_sert[key] = data_org[key]
    data_sert['name'] = name
    data_sert['firstname'] = firstname
    data_sert['lastname'] = lastname
    data_sert['dateborn'] = dateborn
    data_sert['name_suborganization'] = name_suborganization
    data_sert['position'] = position
    data_sert['data_exzam'] = data_exzam
    data_sert['status_exzam'] = status_exzam
    data_sert['theme'] = theme
    data_sert['course_hourses'] = course_hourses

    name_sert, sert_doc = convert_sert(data_sert)
    name_protocol, prot_doc = convert_protocol(data_sert)

    blob_sertificate = sert_doc
    blob_protocol = prot_doc
    return theme2, blob_sertificate, blob_protocol, name_protocol, name_sert


if __name__ == '__main__':
    app.run(debug=True)
