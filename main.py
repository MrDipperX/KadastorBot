import config
from db import PgConn

import telebot
from telebot import types
from telebot.types import InputMediaPhoto

import json
import emoji
from datetime import datetime
import os
import csv
from openpyxl import Workbook


bot = telebot.TeleBot(config.TOKEN)

with open("lang.json", "r", encoding="utf-8") as lang_file:
    lang = json.load(lang_file)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        db_conn = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        bot.send_message(message.from_user.id, f"{emoji.emojize(':Uzbekistan:')} «Toshkent Viloyati Baholash va "
                                               f"Konsalting Markazi, ООО» rasmiy botiga xush kelibsiz!\n\n"
                                               f"{emoji.emojize(':Russia:')} Добро пожаловать в официальный бот "
                                               f"«Toshkent Viloyati Baholash va Konsalting Markazi, ООО»!\n\n"
                                               f"{emoji.emojize(':United_Kingdom:')} Welcome to the official bot "
                                               f"«Toshkent Viloyati Baholash va Konsalting Markazi, ООО»!",
                         parse_mode='html')
        db_conn.create_tables()
        db_conn.add_main_admin()
        db_conn.set_user_temp('no', message.from_user.id)
        db_conn.add_user(message.from_user.id, message.from_user.first_name, message.date)
        user = db_conn.is_old_user(message.from_user.id)
        if user[0] is not None:
            menu(message)
        else:
            choose_lang(message)

    except Exception as e:
        print(e)


def choose_lang(message):
    try:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        uz_btn = types.KeyboardButton(f"{emoji.emojize(':Uzbekistan:')} O'zbekcha")
        ru_btn = types.KeyboardButton(f"{emoji.emojize(':Russia:')} Русский")
        en_btn = types.KeyboardButton(f"{emoji.emojize(':United_Kingdom:')} English")
        keyboard.add(uz_btn, ru_btn, en_btn)
        if get_user_temp(message) == 'no':
            bot.send_message(message.from_user.id, f"{emoji.emojize(':Uzbekistan:')} Tilni tanlang!\n\n"
                                                   f"{emoji.emojize(':Russia:')} Выберите язык!\n\n"
                                                   f"{emoji.emojize(':United_Kingdom:')} Choose language!\n\n",
                             reply_markup=keyboard)
        elif get_user_temp(message) == 'some_lang':
            bot.register_next_step_handler(message, menu)
            bot.send_message(message.from_user.id, f"{lang[get_user_lang(message)]['Choose_lang']}",
                             reply_markup=keyboard)
        else:
            back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} "
                                            f"{lang[get_user_lang(message)]['Back_btn']}")
            keyboard.add(back_btn)
            bot.send_message(message.from_user.id, f"{lang[get_user_lang(message)]['Choose_lang']}",
                             reply_markup=keyboard)
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
        db_conn = PgConn(config.host, config.dbname, config.user, config.port, config.password)
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
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        telp_btn = types.KeyboardButton(
            f"{emoji.emojize(':mobile_phone:')} {lang[get_user_lang(message)]['Telp_numb']}",
            request_contact=True)
        keyboard.add(telp_btn)
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]["Set_phone"], reply_markup=keyboard)
    except Exception as e:
        print(e)


def get_user_lang(message):
    try:
        db_conn = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        user_lang = db_conn.get_user_lang(message.from_user.id)
        return user_lang
    except Exception as e:
        print(e)


def get_user_temp(message):
    try:
        db_conn = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        user_temp = db_conn.get_user_temp(message.from_user.id)
        return user_temp
    except Exception as e:
        print(e)


def set_user_temp(message, temp):
    try:
        db_conn = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db_conn.set_user_temp(temp, message.from_user.id)
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db.add_user_contact(message.from_user.id, message.contact.phone_number)
        menu(message)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['menu'])
def menu(message):
    try:
        set_user_temp(message, "Menu")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        evaluate_btn = types.KeyboardButton(f"{emoji.emojize(':money_bag:')} "
                                            f"{lang[get_user_lang(message)]['Evaluate_btn']}")
        settings_btn = types.KeyboardButton(f"{emoji.emojize(':gear:')} {lang[get_user_lang(message)]['Settings_btn']}")
        about_btn = types.KeyboardButton(f"{emoji.emojize(':bank:')} {lang[get_user_lang(message)]['About_btn']}")
        necessary_docs_btn = types.KeyboardButton(f"{emoji.emojize(':open_file_folder:')} "
                                                  f"{lang[get_user_lang(message)]['Necessary_docs_btn']}")
        keyboard.add(evaluate_btn)
        keyboard.add(about_btn, settings_btn)
        keyboard.add(necessary_docs_btn)
        bot.send_message(message.from_user.id, f"{lang[get_user_lang(message)]['Menu']}", reply_markup=keyboard)
    except Exception as e:
        print(e)


def settings(message):
    try:
        set_user_temp(message, "Settings_panel")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        edit_telp_numb_btn = types.KeyboardButton(f"{emoji.emojize(':mobile_phone:')} "
                                                  f"{lang[get_user_lang(message)]['Edit_telp_numb_btn']}",
                                                  request_contact=True)
        edit_lang_btn = types.KeyboardButton(f"{emoji.emojize(':Uzbekistan:')}/{emoji.emojize(':Russia:')}/"
                                             f"{emoji.emojize(':United_Kingdom:')} "
                                             f"{lang[get_user_lang(message)]['Edit_lang_btn']}")
        edit_fullname_btn = types.KeyboardButton(f"{emoji.emojize(':memo:')} "
                                                 f"{lang[get_user_lang(message)]['Edit_fio']}")
        back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang[get_user_lang(message)]['Back_btn']}")
        keyboard.add(edit_telp_numb_btn, edit_lang_btn, edit_fullname_btn, back_btn)
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Settings_btn'], reply_markup=keyboard)
    except Exception as e:
        print(e)


def about(message):
    try:
        set_user_temp(message, "About_panel")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        adresses_btn = types.KeyboardButton(f"{emoji.emojize(':round_pushpin:')} "
                                            f"{lang[get_user_lang(message)]['Adresses_btn']}")
        contacts_btn = types.KeyboardButton(f"{emoji.emojize(':telephone:')} "
                                            f"{lang[get_user_lang(message)]['Contacts_btn']}")
        why_us_btn = types.KeyboardButton(f"{emoji.emojize(':smiling_face_with_sunglasses:')} "
                                          f"{lang[get_user_lang(message)]['Why_us_btn']}")
        back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang[get_user_lang(message)]['Back_btn']}")
        keyboard.add(why_us_btn)
        keyboard.add(adresses_btn, contacts_btn)
        keyboard.add(back_btn)
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Service_btn'], reply_markup=keyboard)
    except Exception as e:
        print(e)


def evaluation_types(message):
    try:
        txt = ""
        eval_btns = []
        set_user_temp(message, "Evaluate_panel")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang[get_user_lang(message)]['Back_btn']}")

        evals = [lang[get_user_lang(message)]['Evaluate_house'], lang[get_user_lang(message)]['Privatization_house'],
                 lang[get_user_lang(message)]['Evaluate_buildings'], lang[get_user_lang(message)]['Evaluate_estate'],
                 lang[get_user_lang(message)]['Evaluate_auto'],
                 lang[get_user_lang(message)]['Evaluate_estate_deposite'],
                 lang[get_user_lang(message)]['Evaluate_movable_estate'],
                 lang[get_user_lang(message)]['Evaluate_business'],
                 lang[get_user_lang(message)]['Evaluate_real_estate'],
                 lang[get_user_lang(message)]['Evaluate_investments'],
                 lang[get_user_lang(message)]['Revaluate_base_capitals'],
                 lang[get_user_lang(message)]['Evaluate_as_complex']]

        for numb, evaluate in zip(config.numbs, evals):
            txt += f"{numb} - {evaluate}\n"
            eval_btns.append(types.KeyboardButton(numb))

        keyboard.add(*eval_btns, back_btn)

        bot.send_message(message.from_user.id, txt, reply_markup=keyboard)
    except Exception as e:
        print(e)


def some_evaluation(message, time_interval):
    try:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang[get_user_lang(message)]['Back_btn']}")
        photo_btn = types.KeyboardButton(f"{emoji.emojize(':outbox_tray:')} "
                                         f"{lang[get_user_lang(message)]['Send_photo']}")
        keyboard.add(photo_btn, back_btn)
        if get_user_temp(message) == 'eval_9':
            bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Not_final_price'],
                             reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Evaluation_price'],
                             reply_markup=keyboard)
        if get_user_temp(message) != 'eval_8':
            bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Evaluation_time_interval'] +
                             time_interval + f"{lang[get_user_lang(message)]['Hours']}")
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['After_shots'] +
                         emoji.emojize(':outbox_tray:') +
                         lang[get_user_lang(message)]['Send_photo'])
    except Exception as e:
        print(e)


@bot.message_handler(commands=['admin'])
def admin(message):
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        admin_info = db.get_admin_info(message.from_user.id)
        if admin_info[0] is not None:
            db.set_user_temp("admin_panel", message.from_user.id)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            users_btn = types.KeyboardButton(f"{emoji.emojize(':busts_in_silhouette:')} "
                                             f"{lang[get_user_lang(message)]['Users_btn']}")
            ad_btn = types.KeyboardButton(f"{emoji.emojize(':loudspeaker:')} {lang[get_user_lang(message)]['Ad_btn']}")
            keyboard.add(users_btn, ad_btn)
            if admin_info[0] == 111312651:
                admin_btn = types.KeyboardButton(f"{emoji.emojize(':person_in_tuxedo_light_skin_tone:')} "
                                                 f"{lang[get_user_lang(message)]['Admin_btn']}")
                keyboard.add(admin_btn)
            bot.send_message(message.from_user.id, f"Добро пожаловать, {admin_info[1]}!", reply_markup=keyboard)
    except Exception as e:
        print(e)


def add_admin(message):
    try:
        admin_data = message.text.splitlines()
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db.add_admin(admin_data[0], admin_data[1])
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Done_btn'])
    except Exception as e:
        print(e)


def edit_admin(message):
    try:
        admin_data = message.text.splitlines()
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db.edit_admin(admin_data[0], admin_data[1])
        bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Done_btn'])
    except Exception as e:
        print(e)


def delete_admin(message):
    try:
        admin_data = message.text
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
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
            db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
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


@bot.message_handler(content_types=['photo'])
def photo_downloader(message):
    try:
        db_conn = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        now = datetime.now()
        if get_user_temp(message) == 'eval_1':
            directory = f"{config.photos_directory}{lang['ru']['Evaluate_house']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_2':
            directory = f"{config.photos_directory}{lang['ru']['Privatization_house']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_3':
            directory = f"{config.photos_directory}{lang['ru']['Evaluate_buildings']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_4':
            directory = f"{config.photos_directory}{lang['ru']['Evaluate_estate']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_5':
            directory = f"{config.photos_directory}{lang['ru']['Evaluate_auto']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_6':
            directory = f"{config.photos_directory}{lang['ru']['Evaluate_estate_deposite']}/" \
                        f"{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_7':
            directory = f"{config.photos_directory}{lang['ru']['Evaluate_movable_estate']}/" \
                        f"{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_8':
            directory = f"{config.photos_directory}{lang['ru']['Evaluate_business']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_9':
            directory = f"{config.photos_directory}{lang['ru']['Evaluate_real_estate']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_10':
            directory = f"{config.photos_directory}{lang['ru']['Evaluate_investments']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_11':
            directory = f"{config.photos_directory}{lang['ru']['Revaluate_base_capitals']}/" \
                        f"{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_12':
            directory = f"{config.photos_directory}{lang['ru']['Evaluate_as_complex']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'admin_panel':
            directory = config.ads_directory

        else:
            return

        if not os.path.isdir(directory):
            os.makedirs(directory)
        src = f"{directory}/" \
              f"IMG_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}_{now.microsecond}.jpg"
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        if get_user_temp(message) in config.evals:
            db_conn.add_photo(message.from_user.id, src, now, get_user_temp(message))
        elif get_user_temp(message) == 'admin_panel':
            db_conn.add_ad_media(src)
            send_ads()

    except Exception as e:
        print(e)


def send_ads():
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
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


@bot.message_handler(content_types=['animation', 'video'])
def gif_n_video(message):
    try:
        if get_user_temp(message) == 'admin_panel':
            db_conn = PgConn(config.host, config.dbname, config.user, config.port, config.password)
            if message.animation is None:
                file_info = bot.get_file(message.video.file_id)
                name = 'VID'
                type_media = 'mp4'
            else:
                file_info = bot.get_file(message.animation.file_id)
                name = 'GIF'
                type_media = 'gif'
            downloaded_file = bot.download_file(file_info.file_path)
            now = datetime.now()
            if not os.path.isdir(f"{config.ads_directory}"):
                os.makedirs(f"{config.ads_directory}")
            src = f"{config.ads_directory}_{name}_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}_" \
                  f"{now.microsecond}.{type_media}"
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            db_conn.add_ad_media(src)
            send_ads()
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['text'])
def mess(message):
    try:
        get_message_bot = message.text.strip()
        db_conn = PgConn(config.host, config.dbname, config.user, config.port, config.password)

        if get_message_bot == f"{emoji.emojize(':Uzbekistan:')} O'zbekcha":
            if get_user_temp(message) == 'no':
                db_conn.set_user_lang("uz", message.from_user.id)
                go_to_fio(message)
            else:
                db_conn.set_user_lang("uz", message.from_user.id)
                db_conn.set_user_temp('some_lang', message.from_user.id)
                menu(message)

        elif get_message_bot == f"{emoji.emojize(':Russia:')} Русский":
            if get_user_temp(message) == 'no':
                db_conn.set_user_lang("ru", message.from_user.id)
                go_to_fio(message)
            else:
                db_conn.set_user_lang("ru", message.from_user.id)
                db_conn.set_user_temp('some_lang', message.from_user.id)
                menu(message)

        elif get_message_bot == f"{emoji.emojize(':United_Kingdom:')} English":
            if get_user_temp(message) == 'no':
                db_conn.set_user_lang("en", message.from_user.id)
                go_to_fio(message)
            else:
                db_conn.set_user_lang("en", message.from_user.id)
                db_conn.set_user_temp('some_lang', message.from_user.id)
                menu(message)

        elif get_message_bot == f"{emoji.emojize(':gear:')} {lang[get_user_lang(message)]['Settings_btn']}":
            settings(message)

        elif get_message_bot == f"{emoji.emojize(':Uzbekistan:')}/{emoji.emojize(':Russia:')}/" \
                                f"{emoji.emojize(':United_Kingdom:')} {lang[get_user_lang(message)]['Edit_lang_btn']}":
            set_user_temp(message, "Edit_lang")
            choose_lang(message)

        elif get_message_bot == f"{emoji.emojize(':memo:')} {lang[get_user_lang(message)]['Edit_fio']}":
            set_user_temp(message, "Edit_fio")
            go_to_fio(message)

        elif get_message_bot == f"{emoji.emojize(':money_bag:')} {lang[get_user_lang(message)]['Evaluate_btn']}":
            evaluation_types(message)

        elif get_message_bot in config.numbs:
            if get_message_bot == '1':
                set_user_temp(message, "eval_1")
                some_evaluation(message, "24")
            elif get_message_bot == '2':
                set_user_temp(message, "eval_2")
                some_evaluation(message, "12")
            elif get_message_bot == '3':
                set_user_temp(message, "eval_3")
                some_evaluation(message, "48")
            elif get_message_bot == '4':
                set_user_temp(message, "eval_4")
                some_evaluation(message, "48")
            elif get_message_bot == '5':
                set_user_temp(message, "eval_5")
                some_evaluation(message, "12")
            elif get_message_bot == '6':
                set_user_temp(message, "eval_6")
                some_evaluation(message, "48")
            elif get_message_bot == '7':
                set_user_temp(message, "eval_7")
                some_evaluation(message, "24")
            elif get_message_bot == '8':
                set_user_temp(message, "eval_8")
                some_evaluation(message, lang[get_user_lang(message)]['No'])
            elif get_message_bot == '9':
                set_user_temp(message, "eval_9")
                some_evaluation(message, "48")
            elif get_message_bot == '10':
                set_user_temp(message, "eval_10")
                some_evaluation(message, "72")
            elif get_message_bot == '11':
                set_user_temp(message, "eval_11")
                some_evaluation(message, "48")
            elif get_message_bot == '12':
                set_user_temp(message, "eval_12")
                some_evaluation(message, "72")

        elif get_message_bot == f"{emoji.emojize(':outbox_tray:')} {lang[get_user_lang(message)]['Send_photo']}":
            album = db_conn.get_album(message.from_user.id, get_user_temp(message))
            full_name = db_conn.get_user_fullname(message.from_user.id)
            if len(album):
                pics = [InputMediaPhoto(open(pic[4], "rb")) for pic in album]
                bot.send_media_group(config.channel_id, pics)
                bot.send_message(config.channel_id, f"{full_name[0]} {full_name[1]} {full_name[2]}")
                bot.send_message(config.channel_id, get_eval_type(message))
                bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Wait_operators'])
            else:
                bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Wait_operators'])
            menu(message)

        elif get_message_bot == f"{emoji.emojize(':bank:')} {lang[get_user_lang(message)]['About_btn']}":
            about(message)

        elif get_message_bot == f"{emoji.emojize(':round_pushpin:')} {lang[get_user_lang(message)]['Adresses_btn']}":
            bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Organization_adress'])
            bot.send_location(message.from_user.id, config.latitude, config.longitude)

        elif get_message_bot == f"{emoji.emojize(':telephone:')} {lang[get_user_lang(message)]['Contacts_btn']}":
            bot.send_contact(message.from_user.id, "998983114014", "TVBKM")
            bot.send_contact(message.from_user.id, "998951708181", "TVBKM")

        elif get_message_bot == f"{emoji.emojize(':smiling_face_with_sunglasses:')} " \
                                f"{lang[get_user_lang(message)]['Why_us_btn']}":
            bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Why_us'])

        elif get_message_bot == f"{emoji.emojize(':open_file_folder:')} " \
                                f"{lang[get_user_lang(message)]['Necessary_docs_btn']}":
            set_user_temp(message, "Docs_panel")

        elif get_message_bot == f"{emoji.emojize(':busts_in_silhouette:')} {lang[get_user_lang(message)]['Users_btn']}":
            if get_user_temp(message) == 'admin_panel':
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
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':person_in_tuxedo_light_skin_tone:')} " \
                                f"{lang[get_user_lang(message)]['Admin_btn']}":
            if get_user_temp(message) == 'admin_panel':
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                add_btn = types.KeyboardButton(f"{emoji.emojize(':plus:')} {lang[get_user_lang(message)]['Add_btn']}")
                edit_btn = types.KeyboardButton(f"{emoji.emojize(':double_curly_loop:')} "
                                                f"{lang[get_user_lang(message)]['Edit_btn']}")
                delete_btn = types.KeyboardButton(f"{emoji.emojize(':minus:')} "
                                                  f"{lang[get_user_lang(message)]['Delete_btn']}")
                back_btn = types.KeyboardButton(f"{emoji.emojize(':BACK_arrow:')} "
                                                f"{lang[get_user_lang(message)]['Back_btn']}")
                keyboard.add(add_btn, edit_btn, delete_btn, back_btn)
                bot.send_message(message.from_user.id, "Выберите", reply_markup=keyboard)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':loudspeaker:')} {lang[get_user_lang(message)]['Ad_btn']}":
            if get_user_temp(message) == 'admin_panel':
                bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Write_ad_text'])
                bot.register_next_step_handler(message, ad_text)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':plus:')} {lang[get_user_lang(message)]['Add_btn']}":
            if get_user_temp(message) == 'admin_panel':
                bot.send_message(message.from_user.id, "Введите данные нового админа")
                bot.register_next_step_handler(message, add_admin)

        elif get_message_bot == f"{emoji.emojize(':double_curly_loop:')} {lang[get_user_lang(message)]['Edit_btn']}":
            if get_user_temp(message) == 'admin_panel':
                bot.send_message(message.from_user.id, "Введите изминения")
                bot.register_next_step_handler(message, edit_admin)

        elif get_message_bot == f"{emoji.emojize(':minus:')} {lang[get_user_lang(message)]['Delete_btn']}":
            if get_user_temp(message) == 'admin_panel':
                bot.send_message(message.from_user.id, "Введите имя админа")
                bot.register_next_step_handler(message, delete_admin)

        elif get_message_bot == f"{emoji.emojize(':BACK_arrow:')} {lang[get_user_lang(message)]['Back_btn']}":
            admin(message)

        elif get_message_bot == f"{emoji.emojize(':left_arrow:')} {lang[get_user_lang(message)]['Back_btn']}":
            if get_user_temp(message) == 'Edit_lang':
                settings(message)

            elif get_user_temp(message) == 'eval_1' or get_user_temp(message) == 'eval_2' or \
                    get_user_temp(message) == 'eval_3' or get_user_temp(message) == 'eval_4' or \
                    get_user_temp(message) == 'eval_5' or get_user_temp(message) == 'eval_6' or \
                    get_user_temp(message) == 'eval_7' or get_user_temp(message) == 'eval_8' or \
                    get_user_temp(message) == 'eval_9' or get_user_temp(message) == 'eval_10' or \
                    get_user_temp(message) == 'eval_11' or get_user_temp(message) == 'eval_12':
                evaluation_types(message)

            else:
                menu(message)

        else:
            pass
    except Exception as e:
        print(e)


def main_loop():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main_loop()
