from docxtpl import DocxTemplate

def convert_protocol(data):
    doc = DocxTemplate("static/templates_sert/template_protocol.docx")  # наименование файла шаблона + путь
    data_sert = data

    context = {'protocol_N': data_sert['protocol_N'],
               'name_organization': data_sert['name_organization'],
               'name_suborganization': data_sert['name_suborganization'],
               'date_exzam': data_sert['date_exzam'],
               'date_order': data_sert['date_order'],
               'number_order': data_sert['number_order'],
               'name_chairman': data_sert['name_chairman'],
               'position_chairman': data_sert['position_chairman'],
               'name_member_1': data_sert['name_member_1'],
               'position_member_1': data_sert['position_member_1'],
               'name_member_2': data_sert['name_member_2'],
               'position_member_2': data_sert['position_member_2'],
               'name_course': data_sert['name_course'],
               'course_hourses': data_sert['course_hourses'],
               'name_user': data_sert['name_user'],
               'firstname': data_sert['firstname'],
               'lastname': data_sert['lastname'],
               'position': data_sert['position'],
               'status_exzam': data_sert['status_exzam'],
               'number_sert': data_sert['number_sert'],
               'reason_for_checking': data_sert['reason_for_checking'],
               }
    doc.render(context)
    doc.save(f"protocol_n_{data_sert['protocol_N']}.docx")
    return
    # TODO блок проверки наличия папки с удостоверениями -  в БД сохранять сами файлы удочтоверений или сслыки на эти файлы


def convert_sert(data):
    doc = DocxTemplate("static/templates_sert/template_sert.docx")  # наименование файла шаблона
    data_sert = data

    context = {'protocol_N': data_sert['protocol_N'],
               'name_organization': data_sert['name_organization'],
               'name_suborganization': data_sert['name_suborganization'],
               'date_exzam': data_sert['date_exzam'],
               'date_order': data_sert['date_order'],
               'number_order': data_sert['number_order'],
               'name_chairman': data_sert['name_chairman'],
               'position_chairman': data_sert['position_chairman'],
               'name_member_1': data_sert['name_member_1'],
               'position_member_1': data_sert['position_member_1'],
               'name_member_2': data_sert['name_member_2'],
               'position_member_2': data_sert['position_member_2'],
               'name_course': data_sert['name_course'],
               'course_hourses': data_sert['course_hourses'],
               'name_user': data_sert['name_user'],
               'firstname': data_sert['firstname'],
               'lastname': data_sert['lastname'],
               'position': data_sert['position'],
               'status_exzam': data_sert['status_exzam'],
               'number_sert': data_sert['number_sert'],
               'reason_for_checking': data_sert['reason_for_checking'],
               }
    doc.render(context)
    doc.save(f"sertificat_n_{data_sert['protocol_N']}.docx")

    return
