from loader import bot
from db.db import PgConn
from utils.helpers import get_user_temp, send_ads, menu
from utils.lang import lang
from utils.constants import PHOTOS_DIRECTORY, evals, ADS_DIRECTORY

from datetime import datetime
import os


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    try:
        db = PgConn()
        db.add_user_contact(message.from_user.id, message.contact.phone_number)
        menu(message)
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['photo'])
def photo_downloader(message):
    try:
        db_conn = PgConn()
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        now = datetime.now()
        if get_user_temp(message) == 'eval_1':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Evaluate_house']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_2':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Privatization_house']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_3':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Evaluate_buildings']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_4':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Evaluate_estate']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_5':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Evaluate_auto']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_6':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Evaluate_estate_deposite']}/" \
                        f"{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_7':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Evaluate_movable_estate']}/" \
                        f"{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_8':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Evaluate_business']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_9':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Evaluate_real_estate']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_10':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Evaluate_investments']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_11':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Revaluate_base_capitals']}/" \
                        f"{message.from_user.first_name}"

        elif get_user_temp(message) == 'eval_12':
            directory = f"{PHOTOS_DIRECTORY}{lang['ru']['Evaluate_as_complex']}/{message.from_user.first_name}"

        elif get_user_temp(message) == 'admin_panel':
            directory = ADS_DIRECTORY

        else:
            return

        if not os.path.isdir(directory):
            os.makedirs(directory)
        src = f"{directory}/" \
              f"IMG_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}_{now.microsecond}.jpg"
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        if get_user_temp(message) in evals:
            db_conn.add_photo(message.from_user.id, src, now, get_user_temp(message))
        elif get_user_temp(message) == 'admin_panel':
            db_conn.add_ad_media(src)
            send_ads()

    except Exception as e:
        print(e)


@bot.message_handler(content_types=['animation', 'video'])
def gif_n_video(message):
    try:
        if get_user_temp(message) == 'admin_panel':
            db_conn = PgConn()
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
            if not os.path.isdir(f"{ADS_DIRECTORY}"):
                os.makedirs(f"{ADS_DIRECTORY}")
            src = f"{ADS_DIRECTORY}_{name}_{now.year}{now.month}{now.day}_{now.hour}{now.minute}{now.second}_" \
                  f"{now.microsecond}.{type_media}"
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            db_conn.add_ad_media(src)
            send_ads()
    except Exception as e:
        print(e)
