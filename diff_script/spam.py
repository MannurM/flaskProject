#  TODO Вывод на экран ПДФ

# document.add_heading(data['edu_materials'], 0)
# f = StringIO()
# document.save(f)
# hength=f.tell()
# f.seek(0)
# return send_file(f.as_attachment=True, attachment_filename ='report.doc')
# print(data)
# pdf_document = data['edu_materials']
# with open(pdf_document, "rb") as filehandle:
#     pdf = PdfFileReader(filehandle)
#     info = pdf.getDocumentInfo()
#     pages = pdf.getNumPages()
#     print("Количество страниц в документе: %i\n\n" % pages)
#     print("Мета-описание: ", info)
#     page = pdf.getFormTextFields()
#     data['edu_mat'] = page
#
#     for i in range(pages):
#         page = pdf.getPage(i)
#         print("Стр.", i, " мета: ", page, "\n\nСодержание;\n")
#         print(page.extractText())


# with open('/path/of/file.pdf', 'rb') as static_file:
    #     return send_file(static_file, attachment_filename='file.pdf')

    # from flask import send_from_directory, current_app as app
    #
    # @app.route('/show/PDFs/')
    # def send_pdf():
    #     return send_from_directory(app.config['UPLOAD_FOLDER'], 'file.pdf')

    # theme, edu_materials, exsersis, exzamen = dbase.getCourse()
    # name, firstname, lastname, status_course, count_prob = dbase.getStatus(user_id=user_id)



    # from flask import send_from_directory
    # @app.route('/open', methods=['GET', 'POST'])
    # def open():
    #     return send_from_directory(directory='some_directory',
    #                                filename='filename',
    #                                mimetype='application/pdf')



# @app.route('/show_pdf/<user_id>')
# def show_pdf(user_id):
#     global data
#     data = data
#     pdf_document = data['edu_materials']
#     print(pdf_document)
    # with open(pdf_document, 'rb') as file:
    #     return redirect(file)

    # doc = fitz.open(pdf_document)
    # print("Исходный документ: ", doc)
    # print("\nКоличество страниц: %i\n\n------------------\n\n" % doc.pageCount)
    # print(doc.metadata)
    # for current_page in range(len(doc)):
    #     page = doc.loadPage(current_page)
    #     page_text = page.getText("text")
    #     print("Стр. ", current_page + 1, "\n\nСодержание;\n")
    #     print(page_text)

    # with open(pdf_document, "rb") as filehandle:
    #     pdf = PdfFileReader(filehandle)
    #     info = pdf.getDocumentInfo()
    #     pages = pdf.getNumPages()
    #     print("Количество страниц в документе: %i\n\n" % pages)
    #     print("Мета-описание: ", info)
    #     for i in range(pages):
    #         page = pdf.getPage(i)
    #         print("Стр.", i, " мета: ", page, "\n\nСодержание;\n")
    #         print(page.extractText())
    # return send_file(pdf_document, mimetype='pdf')


# @app.route('/edu_test_1/<user_id>', methods=['GET', 'POST'])
# @login_required
# def edu_test_1(user_id):
#     data = status_user(user_id=user_id) # Собирает данные из БД по статистике
#     rd = readTest()  # Создает объект для чтения в него данных
#     sum_just = 0
#     count_qestion = 3
#     # TODO цикл вывода воспросов на страницу должен быть отдельно от количества вопросов и не внутри апроута??
#     # qa_dict = rd.read_test(app.config['DATABASE']) # Наполняет данными объект
#     qa_result = rd.read_test(app.config['DATABASE'])
#     temp_dict = {} # форма для словаря вывода вопрсов и  ответов в шаблон
#     list_answer_just = [] # список правильных ответов
#     print(qa_result)
#     # for label, val in qa_dict.items():
#     #     print('val', val)
#     #     for qestion, answer in val.items():
#     #         answer = ast.literal_eval(answer) # Избавляет от кавычек список
#     #         answer_not_resp = []
#     #         # temp_dict[label] = qestion  # temp.label -  выведет в шаблоне вопрос по индикатору
#     #         answer_len = len(answer)  # количество ответов
#     #         for ans in answer:
#     #             just = ans[-3:]  # признак правильности ответа
#     #             if just == '__1':
#     #                 answer_just = ans[:-3]
#     #                 ans = answer_just  # ответ без признака правильности ответа
#     #                 list_answer_just.append(answer_just) # список правильных ответов
#     #             else:
#     #                 ans = ans[:-3]
#     #             answer_not_resp.append(ans)
#     #
#     #         temp_dict[qestion] = answer_not_resp
#             # print(temp_dict[qestion])
#     if request.method == 'POST':
#         print('post')
#         answer = request.form['answer']
#         if not answer:
#             flash('ОШИБКА, проверьте ввод ответа!')
#         if stat_edu_test(list_answer_just, answer):
#             sum_just += 1
#         print(sum_just)
#         if sum_just >= count_qestion * 0.6:
#             data['status'] = '1'
#         else:
#             data['status'] = '0'
#
#         # TODO запись в БД
#
#     return render_template('edu_test_1.html', data=data,  temp_dict=temp_dict )



# import os
# from flask import Flask, flash, request, redirect, url_for
# # объясняется ниже
# from werkzeug.utils import secure_filename
#
#
# # папка для сохранения загруженных файлов
# UPLOAD_FOLDER = '/path/to/the/uploads'
# # расширения файлов, которые разрешено загружать
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc'}
#
#
# # создаем экземпляр приложения
# app = Flask(__name__)
# # конфигурируем
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
#
# def allowed_file(filename):
#     """ Функция проверки расширения файла """
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # проверим, передается ли в запросе файл
#         if 'file' not in request.files:
#             # После перенаправления на страницу загрузки
#             # покажем сообщение пользователю
#             flash('Не могу прочитать файл')
#             return redirect(request.url)
#         file = request.files['file']
#         # Если файл не выбран, то браузер может
#         # отправить пустой файл без имени.
#         if file.filename == '':
#             flash('Нет выбранного файла')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             # безопасно извлекаем оригинальное имя файла
#             filename = secure_filename(file.filename)
#             # сохраняем файл
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # если все прошло успешно, то перенаправляем
#             # на функцию-представление `download_file`
#             # для скачивания файла
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <title>Загрузить новый файл</title>
#     <h1>Загрузить новый файл</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     </html>
#     '''

# db = get_db()
# dbase = FDataBase(db)
# theme, protocol, sertificate = dbase.read_sertificat(user_id)

# # кодирование в  бинарный пдф

# def write_to_file(data, filename):
#     # Преобразование двоичных данных в нужный формат
#     with open(filename, 'wb') as file:
#         file.write(data)
#     print("Данный из blob сохранены в: ", filename, "\n")

# Конвертация из docx в PDF
# import sys
# import os
# import comtypes.client
# from docxtpl import DocxTemplate
#
# doc = DocxTemplate("шаблон.docx")
# context = { 'emitent' : 'ООО Ромашка', 'address1' : 'г. Москва, ул. Долгоруковская, д. 0', 'участник': 'ООО Участник', 'адрес_участника': 'г. Москва, ул. Полевая, д. 0', 'director': 'И.И. Иванов'}
# doc.render(context)
# doc.save("final.docx")
#
# wdFormatPDF = 17
#
# in_file = os.path.abspath ("final.docx")
# out_file = os.path.abspath("final.pdf")
#
# word = comtypes.client.CreateObject('Word.Application')
# doc = word.Documents.Open(in_file)
# doc.SaveAs(out_file, FileFormat=wdFormatPDF)
# doc.Close()
# word.Quit()


    # def run(self):
    #     convert_path(self, path)
    #     data = create_template_sert(self, prot, sert, theme_in)
    #     db = get_db()
    #     dbase = FDataBase(db)
    #     dbase.create_template_sert(data)

# def save_list_just(self, user_id, list_answer_just):
#     try:
#         # сделать отдельную функцию для создания базы данных со всеми таблицами
#         laj = str(list_answer_just)
#         self.__cur.execute("INSERT INTO a_just (id, laj) VALUES(?, ?)", (user_id, laj))
#     except sqlite3.Error as e:
#         print("Ошибка записи данных в БД(save_list_just) " + str(e))