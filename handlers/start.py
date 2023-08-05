from loader import bot
from db.db import PgConn
import emoji
from utils.helpers import choose_lang, menu


@bot.message_handler(commands=['start'])
def start(message):
    try:
        db_conn = PgConn()
        db_conn.create_tables()
        db_conn.add_main_admin()
        db_conn.set_user_temp('no', message.from_user.id)
        db_conn.add_user(message.from_user.id, message.from_user.first_name, message.date)
        user = db_conn.is_old_user(message.from_user.id)
        if user[0] is not None:
            menu(message)
        else:
            choose_lang(message)
        bot.send_message(message.from_user.id, f"{emoji.emojize(':Uzbekistan:')} «Toshkent Viloyati Baholash va "
                                               f"Konsalting Markazi, ООО» rasmiy botiga xush kelibsiz!\n\n"
                                               f"{emoji.emojize(':Russia:')} Добро пожаловать в официальный бот "
                                               f"«Toshkent Viloyati Baholash va Konsalting Markazi, ООО»!\n\n"
                                               f"{emoji.emojize(':United_Kingdom:')} Welcome to the official bot "
                                               f"«Toshkent Viloyati Baholash va Konsalting Markazi, ООО»!",
                         parse_mode='html')
    except Exception as e:
        print(e)
