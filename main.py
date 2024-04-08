import time
import requests
from binance.um_futures import UMFutures
from tradingview_ta import TA_Handler, Interval, Exchange

INTERVAL = Interval.INTERVAL_15_MINUTES
TELEGRAM_TOKEN = ''
TELEGRAM_CHANNEL = ''

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
    print('Сбор начальных данных...')
    print('\n'.join(symbols))
    send_massage('Сбор начальных данных...')
    for i in symbols:
            try:
                data = get_data(i)
                # print(data)
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

first_data()
print('Погнали')
send_massage('Погнали')

while True:
    print('_______________________Новый цикл______________________')
    for i in symbols:
        try:
            data = get_data(i)
            # print(data)
            if (data['RECOMMENDATION'] == 'STRONG_BUY' and (data['SYMBOL'] not in longs)):
                print(data['SYMBOL'], 'Buy')
                text = data['SYMBOL'] + 'BUY'
                send_massage(text)
                longs.append(data['SYMBOL'])



            if (data['RECOMMENDATION'] == 'STRONG_SELL' and (data['SYMBOL'] not in shorts)):
                print(data['SYMBOL'], 'Sell')
                text = data['SYMBOL'] + 'SELL'
                send_massage(text)
                shorts.append(data['SYMBOL'])
            time.sleep(0.1)
        except:
            pass