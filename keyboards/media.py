from telebot import types


def input_media(album):
    return [types.InputMediaPhoto(open(pic[4], "rb")) for pic in album]
