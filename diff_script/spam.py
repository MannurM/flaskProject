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