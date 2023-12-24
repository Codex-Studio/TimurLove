from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from logging import basicConfig, INFO
from django.conf import settings

from apps.settings.models import Photo, Movie, Complement
from apps.telegram.models import TelegramUser
from apps.telegram.keyboards import start_keyboard

# Create your views here.
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)

"""Функция для обработки комманды /start. Если пользователя нету в базе, 
бот создаст его и даст ему поль пользователя.
По желаю можно сделать его курьером"""
@dp.message_handler(commands='start')
async def start(message: types.Message):
    user_id = message.from_user.id  # Уникальный ID пользователя

    # Используйте только уникальный user_id для get_or_create
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(
        user_id=user_id,
        defaults={
            'username': message.from_user.username,
            'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name,
        }
    )

    if created:
        # Если создан новый пользователь
        await message.answer(f"Привет, новый пользователь {message.from_user.full_name}!", reply_markup=start_keyboard)
    else:
        # Если пользователь уже существует
        await message.answer(f"С возвращением, {message.from_user.full_name}!", reply_markup=start_keyboard)

class Form(StatesGroup):
    waiting_for_photo = State()

@dp.message_handler(text='Добавить фото')
async def get_photo(message: types.Message):
    await message.answer("Отправьте свое фото")
    await Form.waiting_for_photo.set()

@dp.message_handler(content_types=['photo'], state=Form.waiting_for_photo)
async def handle_photo(message: types.Message, state: FSMContext):
    # Получение объекта фотографии
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # Скачивание фотографии
    await bot.download_file(file_path, f"photos/{file_id}.jpg")

    # Создание записи в базе данных
    new_photo = Photo(title=f"Фото от {message.from_user.username}", image=f"photos/{file_id}.jpg")
    await sync_to_async(new_photo.save)()

    await message.answer("Фото сохранено в базе данных")

    # Сброс состояния
    await state.finish()

@dp.message_handler(text='Комплемент')
async def get_complement(message: types.Message):
    complement = await sync_to_async(Complement.get_random)()
    await message.answer(complement.title if complement else "Комплименты закончились :(")

@dp.message_handler(text='Получить фото')
async def send_photo(message: types.Message):
    random_photo = await sync_to_async(Photo.get_random)()

    if random_photo:
        photo_path = random_photo.image.path  # Убедитесь, что это правильный путь к файлу
        await bot.send_photo(message.chat.id, photo=InputFile(photo_path))
    else:
        await message.answer("Извините, фото не найдены.")

class MovieState(StatesGroup):
    title = State()

@dp.message_handler(text='Добавить фильм')
async def get_movie(message:types.Message):
    await message.answer("Введите название фильма которое хотите добавить")
    await MovieState.title.set()

@dp.message_handler(state=MovieState.title)
async def add_movie_db(message: types.Message, state: FSMContext):
    movie_title = message.text  # Получение названия фильма из сообщения

    # Создание и сохранение нового объекта Movie
    new_movie = Movie(title=movie_title)
    await sync_to_async(new_movie.save)()

    await message.answer(f"Фильм '{movie_title}' успешно добавлен в базу данных!")

    # Сброс состояния
    await state.finish()

@dp.message_handler(text='Фильм')
async def get_movie(message: types.Message):
    random_movie = await sync_to_async(Movie.objects.filter(watched=False).order_by('?').first)()

    if random_movie:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton("Смотрели", callback_data=f"watched_{random_movie.id}"))
        await message.answer(f"Фильм: {random_movie.title}", reply_markup=keyboard)
    else:
        await message.answer("Все фильмы просмотрены.")

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('watched_'))
async def mark_movie_watched(callback_query: types.CallbackQuery):
    movie_id = int(callback_query.data.split('_')[1])
    movie = await sync_to_async(Movie.objects.get)(id=movie_id)
    movie.watched = True
    await sync_to_async(movie.save)()

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Фильм '{movie.title}' отмечен как просмотренный.")

@dp.message_handler()
async def not_found(message:types.Message):
    await message.reply('Я вас не понял, введите /start')