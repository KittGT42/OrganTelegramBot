from aiogram import Bot, Dispatcher, executor, types
from PIL import Image, ImageFont, ImageDraw, ImageColor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

bot = Bot('6377679142:AAGuFfzhdgOoZKiTNl_qNgryUSE9E7S6hpg', )
STORAGE = MemoryStorage()
dp = Dispatcher(bot, storage=STORAGE)
TEMPLATE = ''
IMAGE_OUT = ''
DRAW = ''
color = ImageColor.getrgb(ImageColor.colormap.get("white"))


class ProfileInvitation(StatesGroup):
    FULL_NAME = State()
    NUMBER_OF_ROW = State()
    NUMBER_OF_PLACES = State()
    DATE_OF_CONCERT = State()


def make_ticket(fio, numb_row, numb_place, date):
    global IMAGE_OUT, TEMPLATE, DRAW
    TEMPLATE = Image.open("/Users/pro/PycharmProjects/venv_Telegram_Bot_Organ_by_aiogram/"
                          "Template/2023-07-01 16.13.38.jpg")
    IMAGE_OUT = TEMPLATE.resize((1280, 720))
    font = ImageFont.truetype("/Users/pro/PycharmProjects/venv_Telegram_Bot_Organ_by_aiogram/fonts/"
                              "ofont.ru_Times New Roman.ttf", size=40)
    font_for_number = ImageFont.truetype("/Users/pro/PycharmProjects/venv_Telegram_Bot_Organ_by_aiogram/fonts/"
                                         "times new roman.ttf", size=46)
    DRAW = ImageDraw.Draw(IMAGE_OUT)
    DRAW.text((700, 317), fio, font=font_for_number, fill=color)
    DRAW.text((767, 405), numb_row, font=font, fill=color)
    DRAW.text((907, 407), numb_place, font=font, fill=color)
    DRAW.text((1136, 200), date, font=font_for_number, fill=color)
    IMAGE_OUT.save('Probe.png')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('/create'))
    markup.add(types.KeyboardButton('/result'))
    markup.add(types.KeyboardButton('/newly'))
    await message.answer('Все готово до создання броні нажми /create для початку', reply_markup=markup)
    await message.answer('Якщо збилась, для заповнення заново /newly', reply_markup=markup)


@dp.message_handler(commands=['create', 'newly'])
async def take_fio(message: types.Message):
    await message.answer('Напиши ФИО')
    await ProfileInvitation.FULL_NAME.set()


@dp.message_handler(state=ProfileInvitation.FULL_NAME)
async def load_fio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = message.text

    await message.answer('Напиши ряд')
    await ProfileInvitation.next()


@dp.message_handler(state=ProfileInvitation.NUMBER_OF_ROW)
async def load_number_of_row(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_of_row'] = message.text

    await message.answer('Напиши места')
    await ProfileInvitation.next()


@dp.message_handler(state=ProfileInvitation.NUMBER_OF_PLACES)
async def load_number_of_places(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number_of_places'] = message.text

    await message.answer('Напиши дату')
    await ProfileInvitation.next()


@dp.message_handler(state=ProfileInvitation.DATE_OF_CONCERT)
async def load_date_of_concert(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['load_date_of_concert'] = message.text
        make_ticket(fio=data['full_name'], numb_row=data['number_of_row'], numb_place=data['number_of_places'],
                    date=data['load_date_of_concert'])

    await message.answer('Для відправки готової броні нажми на /result')
    await state.finish()


@dp.message_handler(commands=['result'])
async def cmd_result(message: types.Message):
    photo = open('/Users/pro/PycharmProjects/venv_Telegram_Bot_Organ_by_aiogram/Probe.png', 'rb')
    await bot.send_photo(message.chat.id, photo)
    os.remove('/Users/pro/PycharmProjects/venv_Telegram_Bot_Organ_by_aiogram/Probe.png')
    await message.answer('Для створення нового бронювання жми /create')


executor.start_polling(dp)