from aiogram import Bot, Dispatcher, types, executor
from asgiref.sync import sync_to_async
from logging import basicConfig, INFO
from django.conf import settings

from apps.telegram.models import TelegramUser
from apps.telegram.keyboards import start_keyboard

# Create your views here.
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
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

@dp.callback_query_handler(text='Добавить фото')
async def get_photo(message:types.Message):
    await message.answer("Отправьте свое фото")

@dp.message_handler(text='Комплемент')
async def get_complement(message:types.Message):
    await message.answer("Комплемент")

@dp.message_handler(text='Получить фото')
async def send_photo(message:types.Message):
    await message.answer('Вот фото')