# utf-8
import ast
from diff_script.read_test import readTest


def unpacking_edutest(path):
    temp_dict = {}
    list_answer_just = []
    rd = readTest()
    qa_dict = rd.read_test(path)  # модуль чтения данных из БД
    for label, val in qa_dict.items():
        for qestion, answer in val.items():
            answer = ast.literal_eval(answer)  # Избавляет от кавычек список
            answer_not_resp = []
            for ans in answer:
                answer_not_resp.append(ans) # список всех ответов
            temp_dict[qestion] = answer_not_resp  # словарь из ключа - вопроса, значений - вариантов ответов
    return temp_dict, list_answer_just