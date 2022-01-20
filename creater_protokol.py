import os
import tempfile
from docxtpl import DocxTemplate
from docx2pdf import convert

def convert_protocol(data):
    print(os.getcwd())
    doc = DocxTemplate('static/templates_sert/template_protocol.docx')  # наименование файла шаблона + путь
    data_sert = data

    context = {'protocol_N': data_sert['protocol_N'],
               'name_organization': data_sert['name_organization'],
               'name_suborganization': data_sert['name_suborganization'],
               'date_exzam': data_sert['data_exzam'],
               'date_order': data_sert['data_order'],
               'number_order': data_sert['number_order'],
               'name_chairman': data_sert['name_chairman'],
               'position_chairman': data_sert['position_chairman'],
               'name_member_1': data_sert['name_member_1'],
               'position_member_1': data_sert['position_member_1'],
               'name_member_2': data_sert['name_member_2'],
               'position_member_2': data_sert['position_member_2'],
               'name_course': data_sert['theme'],
               'course_hourses': data_sert['course_hourses'],
               'name_user': data_sert['name'],
               'firstname': data_sert['firstname'],
               'lastname': data_sert['lastname'],
               'position': data_sert['position'],
               'status_exzam': data_sert['status_exzam'],
               'number_sert': data_sert['number_sert'],
               'reason_for_checking': data_sert['reason_for_checking'],
               }
    doc.render(context)
    name_sertif = f"protocol_n_{data_sert['protocol_N']}_{data['name']}.pdf"


    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        name_tmpdir_sert = f"{tmpdirname}\protocol_n_{data_sert['protocol_N']}_{data['name']}.docx"
        print(name_tmpdir_sert)
        doc.save(name_tmpdir_sert)
        # TODO конвертировать в ПДФ?? потом перевести в бинарные данные
        pdf = 'sertif.pdf'
        # convert("input.docx")
        convert(doc, pdf)
        # convert("my_docx_folder/")

        with open(name_tmpdir_sert, 'rb') as file:
            pdf = file.read()
            # file.seek(0)
    print('docx_prot!!!', type(pdf), name_sertif)
    # TODO Можно создать сразу здесь бинарный файл, но  он будет docxTemlate -
    return name_sertif, pdf


def convert_sert(data):
    # TODO скачать шаблон из БД, распаковать в досx из blob,
    doc = DocxTemplate("static/templates_sert/template_sert.docx")  # наименование файла шаблона
    data_sert = data

    context = {'protocol_N': data_sert['protocol_N'],
               'name_organization': data_sert['name_organization'],
               'name_suborganization': data_sert['name_suborganization'],
               'date_exzam': data_sert['data_exzam'],
               'date_order': data_sert['data_order'],
               'number_order': data_sert['number_order'],
               'name_chairman': data_sert['name_chairman'],
               'position_chairman': data_sert['position_chairman'],
               'name_member_1': data_sert['name_member_1'],
               'position_member_1': data_sert['position_member_1'],
               'name_member_2': data_sert['name_member_2'],
               'position_member_2': data_sert['position_member_2'],
               'name_course': data_sert['theme'],
               'course_hourses': data_sert['course_hourses'],
               'name_user': data_sert['name'],
               'firstname': data_sert['firstname'],
               'lastname': data_sert['lastname'],
               'position': data_sert['position'],
               'status_exzam': data_sert['status_exzam'],
               'number_sert': data_sert['number_sert'],
               'reason_for_checking': data_sert['reason_for_checking'],
               }
    print("context['protocol_N']", context['protocol_N'])
    doc.render(context)

    with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)

        name_tmpdir_sert = f"{tmpdirname}\sertificat_n_{data_sert['protocol_N']}_{data['name']}.docx"

        print(name_tmpdir_sert)
        doc.save(name_tmpdir_sert)

        name_sertif = f"sertificat_n_{data_sert['protocol_N']}_{data['name']}.docx"
        with open(name_tmpdir_sert,'rb') as file:
            docx = file.read()
    print('docx_sert!!!', type(docx), name_sertif)
    # TODO Можно создать сразу здесь бинарный файл, но  он будет docxTemlate -
    return name_sertif, docx


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

