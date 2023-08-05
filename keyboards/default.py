from telebot import types
import emoji
from utils.lang import lang
# from utils.helpers import get_user_lang
from utils.constants import numbs


# buttons section
def language_buttons(user_lang, user_temp):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    uz_btn = types.KeyboardButton(f"{emoji.emojize(':Uzbekistan:')} O'zbekcha")
    ru_btn = types.KeyboardButton(f"{emoji.emojize(':Russia:')} Русский")
    en_btn = types.KeyboardButton(f"{emoji.emojize(':United_Kingdom:')} English")
    keyboard.add(uz_btn, ru_btn, en_btn)
    if user_temp not in ['no', 'some_lang']:
        back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} "
                                        f"{lang[user_lang]['Back_btn']}")
        keyboard.add(back_btn)
    return keyboard


def telephone_button(user_lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    telp_btn = types.KeyboardButton(f"{emoji.emojize(':mobile_phone:')} {lang[user_lang]['Telp_numb']}",
                                    request_contact=True)
    keyboard.add(telp_btn)
    return keyboard


def menu_buttons(user_lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    evaluate_btn = types.KeyboardButton(f"{emoji.emojize(':money_bag:')} "
                                        f"{lang[user_lang]['Evaluate_btn']}")
    settings_btn = types.KeyboardButton(f"{emoji.emojize(':gear:')} {lang[user_lang]['Settings_btn']}")
    about_btn = types.KeyboardButton(f"{emoji.emojize(':bank:')} {lang[user_lang]['About_btn']}")
    necessary_docs_btn = types.KeyboardButton(f"{emoji.emojize(':open_file_folder:')} "
                                              f"{lang[user_lang]['Necessary_docs_btn']}")
    keyboard.add(evaluate_btn)
    keyboard.add(about_btn, settings_btn)
    keyboard.add(necessary_docs_btn)
    return keyboard


def admin_panel_buttons(user_lang, admin_info):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    users_btn = types.KeyboardButton(f"{emoji.emojize(':busts_in_silhouette:')} "
                                     f"{lang[user_lang]['Users_btn']}")
    ad_btn = types.KeyboardButton(f"{emoji.emojize(':loudspeaker:')} {lang[user_lang]['Ad_btn']}")
    keyboard.add(users_btn, ad_btn)
    if admin_info[0] == 111312651:
        admin_btn = types.KeyboardButton(f"{emoji.emojize(':person_in_tuxedo_light_skin_tone:')} "
                                         f"{lang[user_lang]['Admin_btn']}")
        keyboard.add(admin_btn)
    return keyboard


def admin_buttons(user_lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    add_btn = types.KeyboardButton(f"{emoji.emojize(':plus:')} {lang[user_lang]['Add_btn']}")
    edit_btn = types.KeyboardButton(f"{emoji.emojize(':double_curly_loop:')} "
                                    f"{lang[user_lang]['Edit_btn']}")
    delete_btn = types.KeyboardButton(f"{emoji.emojize(':minus:')} "
                                      f"{lang[user_lang]['Delete_btn']}")
    back_btn = types.KeyboardButton(f"{emoji.emojize(':BACK_arrow:')} "
                                    f"{lang[user_lang]['Back_btn']}")
    keyboard.add(add_btn, edit_btn, delete_btn, back_btn)
    return keyboard


def about_buttons(user_lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    adresses_btn = types.KeyboardButton(f"{emoji.emojize(':round_pushpin:')} "
                                        f"{lang[user_lang]['Adresses_btn']}")
    contacts_btn = types.KeyboardButton(f"{emoji.emojize(':telephone:')} "
                                        f"{lang[user_lang]['Contacts_btn']}")
    why_us_btn = types.KeyboardButton(f"{emoji.emojize(':smiling_face_with_sunglasses:')} "
                                      f"{lang[user_lang]['Why_us_btn']}")
    back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang[user_lang]['Back_btn']}")
    keyboard.add(why_us_btn)
    keyboard.add(adresses_btn, contacts_btn)
    keyboard.add(back_btn)
    return keyboard


def setting_buttons(user_lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    edit_telp_numb_btn = types.KeyboardButton(f"{emoji.emojize(':mobile_phone:')} "
                                              f"{lang[user_lang]['Edit_telp_numb_btn']}",
                                              request_contact=True)
    edit_lang_btn = types.KeyboardButton(f"{emoji.emojize(':Uzbekistan:')}/{emoji.emojize(':Russia:')}/"
                                         f"{emoji.emojize(':United_Kingdom:')} "
                                         f"{lang[user_lang]['Edit_lang_btn']}")
    edit_fullname_btn = types.KeyboardButton(f"{emoji.emojize(':memo:')} "
                                             f"{lang[user_lang]['Edit_fio']}")
    back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang[user_lang]['Back_btn']}")
    keyboard.add(edit_telp_numb_btn, edit_lang_btn, edit_fullname_btn, back_btn)
    return keyboard


def eval_buttons(user_lang):
    txt = ""
    eval_btns = []

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang[user_lang]['Back_btn']}")

    evals = [lang[user_lang]['Evaluate_house'], lang[user_lang]['Privatization_house'],
             lang[user_lang]['Evaluate_buildings'], lang[user_lang]['Evaluate_estate'],
             lang[user_lang]['Evaluate_auto'],
             lang[user_lang]['Evaluate_estate_deposite'],
             lang[user_lang]['Evaluate_movable_estate'],
             lang[user_lang]['Evaluate_business'],
             lang[user_lang]['Evaluate_real_estate'],
             lang[user_lang]['Evaluate_investments'],
             lang[user_lang]['Revaluate_base_capitals'],
             lang[user_lang]['Evaluate_as_complex']]

    for numb, evaluate in zip(numbs, evals):
        txt += f"{numb} - {evaluate}\n"
        eval_btns.append(types.KeyboardButton(numb))

    keyboard.add(*eval_btns, back_btn)
    return keyboard, txt


def some_eval_buttons(user_lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang[user_lang]['Back_btn']}")
    photo_btn = types.KeyboardButton(f"{emoji.emojize(':outbox_tray:')} "
                                     f"{lang[user_lang]['Send_photo']}")
    keyboard.add(photo_btn, back_btn)
    return keyboard
