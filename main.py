import time
import traceback
import telebot
import requests
import os

port = int(os.environ.get('PORT', 5000))

token = "605519378:AAEd0WOYiatGI-Nrf9vK2DLgJdFVD2NpMZc"
bot = telebot.TeleBot(token)

help = 'Hello!Example of commands: btc usd, btc rur, zec usd and etc'

def human_redable(number):
    number = str(int(number))
    number = ','.join(number[i:i + 3] for i in range(0, len(number), 3))
    return number

def get_rate_wex(text):

    try:
        pair_wex = text.replace(' ', '_')
        url = 'https://wex.nz/api/3/ticker/' + pair_wex  # send json request
        response = requests.get(url)
        list = (response.json()[pair_wex])  # get list
        content = dict(list)  # convert to dictionary
        rate = 'Wex: ' + text + ' - ' + str(round(float(content['last']),5))
    except:
        rate = 'Wex: not found'

    return rate

def get_rate_binance(text):
    try:
        pair_binance = text.replace(' ', '').upper()

        if 'USD' in pair_binance:
            pair_binance = pair_binance.replace('USD','USDT')

        url = 'https://api.binance.com/api/v3/ticker/price?symbol=' + pair_binance  # send json request
        response = requests.get(url)
        list = (response.json())  # get list
        content = dict(list)  # convert to dictionary
        rate = 'Binance: ' + text + ' - ' + str(round(float(content['price']),5))
    except:
        rate='Binance: not found'

    return rate

@bot.message_handler(func=lambda msg: True)
def greeting(message):

    try:
        text = message.text  # get user message

        if '/' in text:

            if text=='/start' or text=='/help':

                response = help

            elif text=='/marketcap':

                url = 'https://api.coinmarketcap.com/v2/global/'
                response = requests.get(url)
                list = (response.json())  # get list
                content = dict(list)  # convert to dictionary
                content = content['data']
                marketcap = content['quotes']
                marketcap = marketcap['USD']
                marketcap = human_redable(marketcap['total_market_cap'])

                response = 'Market capitalization: $ ' + marketcap

            else:
                response=''
                response +=  get_rate_wex(text)
                response += '\n'
                response += get_rate_binance(text)

                if response.count('not found')==2:
                    int('error')

            bot.send_message(message.chat.id, response)

    except Exception:

        print('------------------------------------')
        print('Error:\n', traceback.format_exc())

        if message.chat.type != 'group' and message.chat.type != 'supergroup':
            response = 'not valid par'
            bot.send_message(message.chat.id, response)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)