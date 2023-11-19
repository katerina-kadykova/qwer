import telebot
import sqlite3
from telebot import types
from telebot.types import WebAppInfo

bot = telebot.TeleBot('6414723122:AAHZ-r7KqxnWnbXSPlx0_h13L2m6978pOmg')
conn = sqlite3.connect("D:\OPNET_license\SQLite.db", check_same_thread=False)
cur = conn.cursor()

web_park = WebAppInfo(url="https://katerina-kadykova.github.io/qwer/")



@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_parks = types.KeyboardButton('Парки', web_app=web_park)

        markup.add(btn_parks)
        bot.send_message(message.from_user.id, 'Выберите интересующую вас категорию достопримечательностей', reply_markup=markup)


@bot.message_handler(content_types='web_app_data')
def buy_process(web_app_message):
    a = web_app_message.web_app_data.button_text

    if a == 'Парки':
        a = 'PARKS'
    elif a == 'Памятники':
        a = 'MONUMENTS'
    elif a == 'Знаковые места':
        a = 'PLACES'

    bot.send_message(web_app_message.chat.id,
                     f'{conn.execute(f"Select NAME from {a} WHERE id == {web_app_message.web_app_data.data}").fetchone()[0]}\n\n'
                     f'{conn.execute(f"Select DISC from {a} WHERE id == {web_app_message.web_app_data.data}").fetchone()[0]}')

    x = conn.execute(f"Select LAT, LEN from {a} WHERE id == {web_app_message.web_app_data.data}").fetchone()
    bot.send_location(web_app_message.chat.id, x[0], x[1])


bot.polling(none_stop=True, interval=0)

