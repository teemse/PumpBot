import time
import requests
from binance.um_futures import UMFutures
from tradingview_ta import TA_Handler, Interval, Exchange


INTERVAL = Interval.INTERVAL_15_MINUTES
TELEGRAM_TOKEN = '5589040240:AAHIgpie9Rz7Hxa7SPp-P6T3TwZp2tCMEjk'
TELEGRAM_CHANNEL = '@teemsee'

client = UMFutures()

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

def send_massage(text):
    res = requests.get('https://api.telegram.org/bot{}/sendMassage'.format(TELEGRAM_TOKEN), params=dict(
    chat_id=TELEGRAM_CHANNEL, text=text))
    

symbols = get_symbols()
longs = []
shorts= []


def first_data():
    print('Поиск начальных данных')
    send_massage('Поиск начальных данных')
    for i in symbols:
        try:
            data = get_data(i)
            print(data)
            if (data['RECOMMENDATION'] == 'STRONG_BUY'):
                longs.append(data['SYMBOL'])
                print(data['SYMBOL'], 'Buy')
            
            if (data['RECOMMENDATION'] == 'STRONG_SELL'):
                shorts.append(data['SYMBOL'])
            time.sleep(0.01)
        except:
            pass
    print('longs:')
    print(longs)
    print('shorts:')
    print(shorts)
    return longs, shorts

print('Погнали')
send_massage('Погнали')
first_data()

while True:
    print('_______________________Новый цикл______________________')
    for i in symbols:
        try:
            data = get_data(i)
            # print(data)
            if (data['RECOMMENDATION'] == 'STRONG_BUY' and (data['SUMBOL'] not in longs)):
                print(data['SUMBOL'], 'Buy')
                text = data['SUMBOL'] + 'Buy'
                send_massage(text)
                longs.append(data['SUMBOL'])



            if (data['RECOMMENDATION'] == 'STRONG_SELL' and (data['SUMBOL'] not in shorts)):
                print(data['SUMBOL'], 'Sell')
                text = data['SUMBOL'] + 'SELL'
                send_massage(text)
                longs.append(data['SUMBOL'])
            time.sleep(0.1)
        except:
            pass