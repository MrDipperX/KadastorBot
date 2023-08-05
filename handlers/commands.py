from loader import bot
from db.db import PgConn
from utils.helpers import menu, get_user_lang
from keyboards.default import admin_panel_buttons


@bot.message_handler(commands=['menu'])
def menu_handler(message):
    menu(message)


@bot.message_handler(commands=['admin'])
def admin(message):
    try:
        db = PgConn()
        admin_info = db.get_admin_info(message.from_user.id)
        if admin_info[0] is not None:
            db.set_user_temp("admin_panel", message.from_user.id)
            bot.send_message(message.from_user.id, f"Добро пожаловать, {admin_info[1]}!",
                             reply_markup=admin_panel_buttons(get_user_lang(message), admin_info))
    except Exception as e:
        print(e)
