import time
import traceback
import telebot
import requests
import os

port = int(os.environ.get('PORT', 5000))

token = "605519378:AAEd0WOYiatGI-Nrf9vK2DLgJdFVD2NpMZc"
bot = telebot.TeleBot(token)

donate = '''
You can support creator:
Bitcoin:
16gzM2uGF8WyfamRrwNQdFCpKBe8b7zvw9
Ethereum:
0x962f70bDb0B9Dccd86249385408359fb5136b27D
Litecoin:
LPvJjwK8hVumbDQ9ijGPS1AKSDqFy169fT
Dash:
XnNjRFm3XF5qfj1TPRhdcdGXVEDi5ZNhJV
Zcash:
t1HxXL9NGxmUsXDq1SBRmpXUMc4twbok4j1
'''

help = '''
✅ This bot can give you crypto rates
✅ Need help? /help
✅ You can add bot to chat
For example: btc usd, zec btc, etc
—————————————
If you need your own bot please contact me:
Creator: @semyon_bitcoin
—————————————
Bitcoin donate:
16gzM2uGF8WyfamRrwNQdFCpKBe8b7zvw9
Litecoin donate:
LPvJjwK8hVumbDQ9ijGPS1AKSDqFy169fT
'''

def human_redable(number):
    number = str(int(number))
    number = ','.join(number[i:i + 3] for i in range(0, len(number), 3))
    return number

def get_rate_wex(text):

    try:
        pair_wex = text.replace(' ', '_').lower()
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

        if text=='/start' or text=='/help' or text== '/help@crypto_costs_bot':

            response = help

        elif text=='/donate' or text=='/donate@crypto_costs_bot':

            response =  donate

        elif text=='/marketcap' or text=='/marketcap@crypto_costs_bot':

            url = 'https://api.coinmarketcap.com/v2/global/'
            response = requests.get(url)
            list = (response.json())  # get list
            content = dict(list)  # convert to dictionary
            content = content['data']
            marketcap = content['quotes']
            marketcap = marketcap['USD']
            marketcap = human_redable(marketcap['total_market_cap'])

            response = 'Market capitalization: $ ' + marketcap

        elif text == '/marketcap24h' or text == '/marketcap24h@crypto_costs_bot':

            url = 'https://api.coinmarketcap.com/v2/global/'
            response = requests.get(url)
            list = (response.json())  # get list
            content = dict(list)  # convert to dictionary
            content = content['data']
            volume24 = content['quotes']
            volume24 = volume24['USD']
            volume24 = human_redable(volume24['total_volume_24h'])

            response = '24h Market volume: $ ' + volume24

        elif text == '/allcrypto' or text == '/allcrypto@crypto_costs_bot':

            url = 'https://api.coinmarketcap.com/v2/global/'
            response = requests.get(url)
            list = (response.json())  # get list
            content = dict(list)  # convert to dictionary
            content = content['data']
            allcrypto = content['active_cryptocurrencies']

            response = 'Number of cryptocurrencies: ' + str(allcrypto)


        elif text=='/btcdomimation' or text=='/btcdomimation@crypto_costs_bot':

            url = 'https://api.coinmarketcap.com/v2/global/'
            response = requests.get(url)
            list = (response.json())  # get list
            content = dict(list)  # convert to dictionary
            content = content['data']
            btcdom = content['bitcoin_percentage_of_market_cap']

            response = 'Domination of bitcoin: ' + str(btcdom) + '%'

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
            response = 'not valid par or command'
            bot.send_message(message.chat.id, response)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)