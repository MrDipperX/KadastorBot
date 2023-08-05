from loader import bot
import handlers


def main_loop():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main_loop()
