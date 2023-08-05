from loader import bot
from db.db import PgConn
import emoji
from handlers.commands import admin
from utils.lang import lang
from keyboards.media import input_media
from utils.constants import numbs, OFFICE_LATITUDE, OFFICE_LONGITUDE, ORGANIZATION_TELEPHONE_NUMBERS, \
    ORGANIZATION_SHORT_NAME
from config.config import CHANNEL_ID
from keyboards.default import admin_buttons
from utils.helpers import choose_lang, get_user_lang, get_user_temp, go_to_fio, settings, set_user_temp, menu, \
    some_evaluation, evaluation_types, excel_maker, get_eval_type, about, ad_text, add_admin, edit_admin, delete_admin


@bot.message_handler(content_types=['text'])
def mess(message):
    try:
        get_message_bot = message.text.strip()
        db_conn = PgConn()

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

        elif get_message_bot in numbs:
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
                pics = input_media(album)
                bot.send_media_group(CHANNEL_ID, pics)
                bot.send_message(CHANNEL_ID, f"{full_name[0]} {full_name[1]} {full_name[2]}")
                bot.send_message(CHANNEL_ID, get_eval_type(message))
                bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Wait_operators'])
            else:
                bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Wait_operators'])
            menu(message)

        elif get_message_bot == f"{emoji.emojize(':bank:')} {lang[get_user_lang(message)]['About_btn']}":
            about(message)

        elif get_message_bot == f"{emoji.emojize(':round_pushpin:')} {lang[get_user_lang(message)]['Adresses_btn']}":
            bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Organization_adress'])
            bot.send_location(message.from_user.id, OFFICE_LATITUDE, OFFICE_LONGITUDE)

        elif get_message_bot == f"{emoji.emojize(':telephone:')} {lang[get_user_lang(message)]['Contacts_btn']}":
            for tel_numb in ORGANIZATION_TELEPHONE_NUMBERS:
                bot.send_contact(message.from_user.id, tel_numb, ORGANIZATION_SHORT_NAME)

        elif get_message_bot == f"{emoji.emojize(':smiling_face_with_sunglasses:')} " \
                                f"{lang[get_user_lang(message)]['Why_us_btn']}":
            bot.send_message(message.from_user.id, lang[get_user_lang(message)]['Why_us'])

        elif get_message_bot == f"{emoji.emojize(':open_file_folder:')} " \
                                f"{lang[get_user_lang(message)]['Necessary_docs_btn']}":
            set_user_temp(message, "Docs_panel")

        elif get_message_bot == f"{emoji.emojize(':busts_in_silhouette:')} {lang[get_user_lang(message)]['Users_btn']}":
            if get_user_temp(message) == 'admin_panel':
                excel_maker(message)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':person_in_tuxedo_light_skin_tone:')} " \
                                f"{lang[get_user_lang(message)]['Admin_btn']}":
            if get_user_temp(message) == 'admin_panel':
                bot.send_message(message.from_user.id, "Выберите", reply_markup=admin_buttons(message))
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
