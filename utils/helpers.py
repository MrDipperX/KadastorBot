from loader import bot
from db.db import PgConn
import emoji
from utils.lang import lang
from keyboards.default import about_buttons, eval_buttons, some_eval_buttons, language_buttons, setting_buttons, \
    telephone_button
import csv
from openpyxl import Workbook
from keyboards.default import menu_buttons


def menu(message):
    try:
        set_user_temp(message, "Menu")
        bot.send_message(message.from_user.id, f"{lang[get_user_lang(message)]['Menu']}",
                         reply_markup=menu_buttons(get_user_lang(message)))
    except Exception as e:
        print(e)


def about(message):
    try:
        set_user_temp(message, "About_panel")
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Service_btn'],
                         reply_markup=about_buttons(get_user_lang(message)))
    except Exception as e:
        print(e)


def evaluation_types(message):
    try:
        set_user_temp(message, "Evaluate_panel")
        keyboard, txt = eval_buttons(get_user_lang(message))

        bot.send_message(message.from_user.id, txt, reply_markup=keyboard)
    except Exception as e:
        print(e)


def some_evaluation(message, time_interval):
    try:
        if get_user_temp(message) == 'eval_9':
            bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Not_final_price'],
                             reply_markup=some_eval_buttons(get_user_lang(message)))
        else:
            bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Evaluation_price'],
                             reply_markup=some_eval_buttons(get_user_lang(message)))
        if get_user_temp(message) != 'eval_8':
            bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Evaluation_time_interval'] +
                             time_interval + f"{lang[get_user_lang(message)]['Hours']}")
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['After_shots'] +
                         emoji.emojize(':outbox_tray:') +
                         lang[get_user_lang(message)]['Send_photo'])
    except Exception as e:
        print(e)


def add_admin(message):
    try:
        admin_data = message.text.splitlines()
        db = PgConn()
        db.add_admin(admin_data[0], admin_data[1])
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Done_btn'])
    except Exception as e:
        print(e)


def edit_admin(message):
    try:
        admin_data = message.text.splitlines()
        db = PgConn()
        db.edit_admin(admin_data[0], admin_data[1])
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Done_btn'])
    except Exception as e:
        print(e)


def delete_admin(message):
    try:
        admin_data = message.text
        db = PgConn()
        db.delete_admin(admin_data[0])
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Done_btn'])
    except Exception as e:
        print(e)


def ad_text(message):
    try:
        if message.text == f"{emoji.emojize(':busts_in_silhouette:')} {lang[get_user_lang(message)]['Users_btn']}" or\
                message.text == f"{emoji.emojize(':loudspeaker:')} {lang[get_user_lang(message)]['Ad_btn']}" or\
                message.text == f"{emoji.emojize(':person_in_tuxedo_light_skin_tone:')} " \
                                f"{lang[get_user_lang(message)]['Admin_btn']}":
            return
        else:
            db = PgConn()
            db.add_ad_text(message.text)
            bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Send_media'])
    except Exception as e:
        print(e)


def get_eval_type(message):
    evals = [lang['ru']['Evaluate_house'], lang['ru']['Privatization_house'], lang['ru']['Evaluate_buildings'],
             lang['ru']['Evaluate_estate'], lang['ru']['Evaluate_auto'], lang['ru']['Evaluate_estate_deposite'],
             lang['ru']['Evaluate_movable_estate'], lang['ru']['Evaluate_business'], lang['ru']['Evaluate_real_estate'],
             lang['ru']['Evaluate_investments'], lang['ru']['Revaluate_base_capitals'],
             lang['ru']['Evaluate_as_complex']]

    for i in range(len(evals)):
        if get_user_temp(message) == f'eval_{i+1}':
            return evals[i]


def send_ads():
    try:
        db = PgConn()
        users = db.get_user_info()
        text_and_url = db.send_add()
        file_ext = text_and_url[1].split('.')[1]

        for i in range(len(users)):
            if file_ext == 'jpg':
                bot.send_photo(users[i - 1][1], open(f"{text_and_url[1]}", 'rb'), text_and_url[0])
            elif file_ext == 'gif':
                bot.send_animation(users[i - 1][1], open(f"{text_and_url[1]}", 'rb'), caption=text_and_url[0])
            elif file_ext == 'mp4':
                bot.send_video(users[i - 1][1], open(f"{text_and_url[1]}", 'rb'), caption=text_and_url[0])
    except Exception as e:
        print(e)


def excel_maker(message):
    db_conn = PgConn()
    with open('users.csv', 'w', newline='', encoding="UTF-8") as u:
        writer_header = csv.DictWriter(u, fieldnames=["ID", "ID_Telegram", "Имя пользователся в телеграм",
                                                      "Дата регестрации", "Номер телефона"])
        writer_header.writeheader()
        writer = csv.writer(u)
        writer.writerows(db_conn.get_user_info())
        u.close()
    wb = Workbook()
    ws = wb.active
    with open('users.csv', 'r', encoding="UTF-8") as f:
        for row in csv.reader(f):
            ws.append(row)
    f.close()
    wb.save('users.xlsx')
    users_xlsx = open("users.xlsx", "rb")
    bot.send_document(message.chat.id, users_xlsx)
    users_xlsx.close()


def choose_lang(message):
    try:
        if get_user_temp(message) == 'no':
            bot.send_message(message.from_user.id, f"{emoji.emojize(':Uzbekistan:')} Tilni tanlang!\n\n"
                                                   f"{emoji.emojize(':Russia:')} Выберите язык!\n\n"
                                                   f"{emoji.emojize(':United_Kingdom:')} Choose language!\n\n",
                             reply_markup=language_buttons(get_user_lang(message), get_user_temp(message)))
        elif get_user_temp(message) == 'some_lang':
            bot.register_next_step_handler(message, menu)
            bot.send_message(message.from_user.id, f"{lang[get_user_lang(message)]['Choose_lang']}",
                             reply_markup=language_buttons(get_user_lang(message), get_user_temp(message)))
        else:
            bot.send_message(message.from_user.id, f"{lang[get_user_lang(message)]['Choose_lang']}",
                             reply_markup=language_buttons(get_user_lang(message), get_user_temp(message)))
    except Exception as e:
        print(e)


def get_user_lang(message):
    try:
        db_conn = PgConn()
        user_lang = db_conn.get_user_lang(message.from_user.id)
        return user_lang
    except Exception as e:
        print(e)


def get_user_temp(message):
    try:
        db_conn = PgConn()
        user_temp = db_conn.get_user_temp(message.from_user.id)
        return user_temp
    except Exception as e:
        print(e)


def set_user_temp(message, temp):
    try:
        db_conn = PgConn()
        db_conn.set_user_temp(temp, message.from_user.id)
    except Exception as e:
        print(e)


def go_to_fio(message):
    try:
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Set_fio'])
        bot.register_next_step_handler(message, set_fio)
    except Exception as e:
        print(e)


def set_fio(message):
    try:
        full_name = message.text.split(' ', 2)
        db_conn = PgConn()
        db_conn.set_user_fullname(message.from_user.id, full_name[0], full_name[1], full_name[2])
        if get_user_temp(message) == 'no':
            set_telp(message)
        else:
            menu(message)
    except (Exception, IndexError) as e:
        print(e)
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]["Error_in_fio"])
        go_to_fio(message)


def set_telp(message):
    try:
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]["Set_phone"],
                         reply_markup=telephone_button(get_user_lang(message)))
    except Exception as e:
        print(e)


def settings(message):
    try:
        set_user_temp(message, "Settings_panel")

        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Settings_btn'],
                         reply_markup=setting_buttons(get_user_lang(message)))
    except Exception as e:
        print(e)
