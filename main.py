# импорты
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config_reader import config
from aiogram import F
import time
import requests
from binance.um_futures import UMFutures
from tradingview_ta import TA_Handler, Interval, Exchange

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
# Для записей с типом Secret* необходимо 
# вызывать метод get_secret_value(), 
# чтобы получить настоящее содержимое вместо '*******'
bot = Bot(token=config.bot_token.get_secret_value())

# Диспетчер
dp = Dispatcher()

INTER=[Interval.INTERVAL_1_MINUTE, 
       Interval.INTERVAL_5_MINUTES,
       Interval.INTERVAL_15_MINUTES,
       Interval.INTERVAL_30_MINUTES,
       Interval.INTERVAL_1_HOUR,
       Interval.INTERVAL_2_HOURS,
       Interval.INTERVAL_4_HOURS,
       Interval.INTERVAL_1_DAY,
       Interval.INTERVAL_1_WEEK,
       Interval.INTERVAL_1_MONTH]

INTERVAL = Interval.INTERVAL_15_MINUTES

client = UMFutures()

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
async def forex(message: types.Message):
    await message.reply("Охуел что ли")
    await message.answer("Пока ебнутый", reply_markup=types.ReplyKeyboardRemove())

@dp.message(F.text.lower() == "binance")
async def binance(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Понял"),
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Быстрее"
    )
    await message.answer("Ожидай отец, скамлю мамонтов...", reply_markup=types.ReplyKeyboardRemove())
    first_data()
    await message.answer("Эти не берем", reply_markup=keyboard)
    await message.answer( ','.join(map(str, longs)))
    await message.answer(','.join(map(str, shorts)))

def get_data(symbol):
    output = TA_Handler(symbol=symbol,
                        screener = 'Crypto',
                        exchange = 'Binance',
                        interval = INTERVAL)
    
    activiti = output.get_analysis().summary
    activiti['SYMBOL'] = symbol
    return activiti

def get_symbols():
    tickers = client.mark_price()
    symbols = []
    for i in tickers:
        ticker = i['symbol']
        symbols.append(ticker)
    return symbols

symbols = get_symbols()
longs = []
shorts= []

def first_data():
    print('Сбор начальных данных...')
    print('\n'.join(symbols))
    for i in symbols:
            try:
                data = get_data(i)
                print(data)
                if (data['RECOMMENDATION'] == 'STRONG_BUY'):
                    longs.append(data['SYMBOL'])
                    # print(data['SYMBOL'], 'Buy')
            
                if (data['RECOMMENDATION'] == 'STRONG_SELL'):
                    shorts.append(data['SYMBOL'])
                    # print(data['SYMBOL'], 'Sell')
            except:
                pass
    print('Лонг:')
    print(longs)
    print('Шорт:')
    print(shorts)
    return longs, shorts

@dp.message(F.text.lower() == "понял")
async def basic(message: types.Message):
    while True:
        print('_______________________Новый цикл______________________')
        await message.answer("Ну погнали!")
        await message.answer("_______________Новый цикл______________!", reply_markup=types.ReplyKeyboardRemove())

        for i in symbols:
            try:
                data = get_data(i)
                print(data)
                if (data['RECOMMENDATION'] == 'STRONG_BUY' and (data['SYMBOL'] not in longs)):
                    print(data['SYMBOL'], ' Брать надо')
                    text = data['SYMBOL'] + ' Брать надо'
                    await message.answer(text)
                    longs.append(data['SYMBOL'])



                if (data['RECOMMENDATION'] == 'STRONG_SELL' and (data['SYMBOL'] not in shorts)):
                    print(data['SYMBOL'], ' Продаем нахуй')
                    text = data['SYMBOL'] + ' Продаем нахуй'
                    await message.answer(text)
                    shorts.append(data['SYMBOL'])
                time.sleep(0.1)
            except:
                pass

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
