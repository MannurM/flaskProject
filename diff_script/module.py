# utf-8
import ast
from diff_script.read_test import readTest
from FDataBase import FDataBase, readTest
from project_web_Flask_2 import dbase


# Модуль для проверки результатов тестов
# TODO есть необходимость считать общее количество правильных ответов!!!
def check_edu_test(list_answer_just, data_answer):
    sum_just = 0
    for answer in data_answer:
        if answer in list_answer_just:
            sum_just += 1
            print('good answer!!!')
            print(sum_just)
        else:
            print('no good!')
    return sum_just


# Внутренние функции
# Считывание статистики по ID
def status_user(user_id=None):
    name, firstname, lastname = dbase.getStatus_name(user_id=user_id)
    status_exzam, count_prob = dbase.getStatus_exzam(user_id=user_id)
    id_course, theme, edu_materials, edu_other, edu_additional = dbase.getCourse()
    data = {
        'id_course': id_course,
        'theme': theme,
        'edu_materials': edu_materials,
        'edu_other': edu_other,
        'exzamen': edu_additional,
        'status': status_exzam,
        'count_prob': count_prob,
        'name': name,
        'firstname': firstname,
        'lastname': lastname,
        'user_id': user_id,
        'sum_just': 0,
    }
    return data


# Распаковка теста из БД
def unpacking_edutest(user_id):
    temp_dict = {}
    list_answer_just = []
    rd = readTest()
    qa_dict, dict_just, list_label_use = rd.read_test('pr_ot.db')  # TODO в основной модуль чтения БД
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
    list_label_just = FDataBase.read_list_just(user_id)
    if not list_label_just:
        print('не прочитались данные')
    list_answer_just = []
    list_label_use = []
    for i in list_label_just:
        laj = tuple(i)
        list_answer_just = laj[0]
        list_label_use = laj[1]
    sum_just = check_edu_test(list_answer_just, data_answer)  # модуль проверки формы
    print("количество правильных ответов-", sum_just)
    # TODO это для экзаменационных ответов - там нужен счетчик проб
    # count_prob = dbase.read_count_prob(user_id)
    # data['count_prob'] = count_prob[0]
    # # TODO вызвать из БД - показания счетчика проб
    # print("data['count_prob']", data['count_prob'])
    # count_prob = data['count_prob'] + 1
    # data['count_prob'] = count_prob  # TODO сделать изменяемый счетчик проб

    # dbase.save_status_user(user_id=user_id, data=data)  # TODO записывать в БД полное изменение всех параметоров?
    return sum_just, list_answer_just, data_answer, list_label_use


def check_save_profile(user_id, save_profile, profile_data):
    for key, values in profile_data.items():
        if values != save_profile[key]:
            profile_data[key] = save_profile[key]
    profile_data = profile_data
    FDataBase.update_profile(user_id, profile_data)
    return profile_data



