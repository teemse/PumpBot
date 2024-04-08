# импорты
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config_reader import config
from aiogram import F
from main import first_data, longs, shorts

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
# Для записей с типом Secret* необходимо 
# вызывать метод get_secret_value(), 
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.bot_token.get_secret_value())

# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Binance"),
            types.KeyboardButton(text="Forex")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите биржу"
    )
    await message.answer("Кого ебать будем?", reply_markup=keyboard)

@dp.message(F.text.lower() == "forex")
async def without_puree(message: types.Message):
    await message.reply("Охуел что ли")
    await message.reply("Пока ебнутый", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text.lower() == "binance")
async def with_puree(message: types.Message):
    await message.reply("Ну погнали!")
    await message.answer("Ожидай отец, скамлю мамонтов...", reply_markup=types.ReplyKeyboardRemove())
    first_data()
    await message.answer("На эти не смотри нахуй")
    await message.answer( ','.join(map(str, longs)))
    await message.answer(','.join(map(str, shorts)))
    print('Погнали')

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
