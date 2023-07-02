import os

from telebot import telebot, types
import PIL
from PIL import Image, ImageFont, ImageDraw, ImageColor

images_stock = Image.open("/Users/pro/PycharmProjects/venv_Telegram_Bot_Organ/2023-07-01 16.13.38.jpg")
IMAGES_OUT = images_stock.resize((1280, 720))
FULL_NAME = ''
NUMBER_OF_ROW = ''
NUMBER_OF_PLACES = ''
DATE_OF_CONCERT = ''
font = ImageFont.truetype("/Users/pro/PycharmProjects/pythonProject/PythonFileProject/Vadim Shandriy/lesson_013/"
                          "python_snippets/fonts/ofont.ru_Times New Roman.ttf", size=40)
font_for_number = ImageFont.truetype("/Users/pro/PycharmProjects/pythonProject/PythonFileProject/Vadim Shandriy/"
                                     "lesson_013/python_snippets/fonts/times new roman.ttf", size=46)
DRAW = ImageDraw.Draw(IMAGES_OUT)
color = ImageColor.getrgb(ImageColor.colormap.get("white"))


def make_ticket(fio, numb_row, numb_place, date):
    global IMAGES_OUT
    DRAW.text((700, 317), fio, font=font_for_number, fill=color)
    DRAW.text((767, 405), numb_row, font=font, fill=color)
    DRAW.text((907, 407), numb_place, font=font, fill=color)
    DRAW.text((1136, 200), date, font=font_for_number, fill=color)
    IMAGES_OUT.save('Probe.png')


BOT = telebot.TeleBot('6377679142:AAGuFfzhdgOoZKiTNl_qNgryUSE9E7S6hpg')
COUNTER = 0


@BOT.message_handler(commands=['start'])
def start(message):
    marup = types.ReplyKeyboardMarkup()
    bttn_clean = types.KeyboardButton('/clean_up')
    bttn_result = types.KeyboardButton('/result')
    marup.row(bttn_clean, bttn_result)
    BOT.send_message(message.chat.id, f'Привет нажми на кнопку /clean_up для начала заполнения брони', parse_mode='html')
    BOT.send_message(message.chat.id, f'когда закончишь нажми /result', reply_markup=marup)


@BOT.message_handler(commands=['clean_up'])
def clean_up(message):
    global COUNTER, IMAGES_OUT, DRAW, images_stock
    COUNTER = 0
    images_stock = Image.open("/Users/pro/PycharmProjects/venv_Telegram_Bot_Organ/2023-07-01 16.13.38.jpg")
    IMAGES_OUT = images_stock.resize((1280, 720))
    DRAW = ImageDraw.Draw(IMAGES_OUT)
    BOT.send_message(message.chat.id, f'Теперь начинай вводить ФИО, номер ряда, номер места/мест,'
                                      f' дату концерта по очереди',
                     parse_mode='html')


@BOT.message_handler(commands=['result'])
def result(message):
    global FULL_NAME, NUMBER_OF_ROW, NUMBER_OF_PLACES, DATE_OF_CONCERT
    make_ticket(fio=FULL_NAME, numb_row=NUMBER_OF_ROW, numb_place=NUMBER_OF_PLACES, date=DATE_OF_CONCERT)
    photo = open('/Users/pro/PycharmProjects/venv_Telegram_Bot_Organ/TelegramBotOrgan/Probe.png', 'rb')
    BOT.send_photo(message.chat.id, photo)
    os.remove('/Users/pro/PycharmProjects/venv_Telegram_Bot_Organ/TelegramBotOrgan/Probe.png')


@BOT.message_handler()
def get_user_date(message):
    global COUNTER, FULL_NAME, NUMBER_OF_ROW, NUMBER_OF_PLACES, DATE_OF_CONCERT
    COUNTER += 1
    if COUNTER == 1:
        FULL_NAME = message.text
    elif COUNTER == 2:
        NUMBER_OF_ROW = message.text
    elif COUNTER == 3:
        NUMBER_OF_PLACES = message.text
    elif COUNTER == 4:
        DATE_OF_CONCERT = message.text


BOT.polling(none_stop=True)