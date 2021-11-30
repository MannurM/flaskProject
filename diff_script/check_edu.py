# utf-8
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