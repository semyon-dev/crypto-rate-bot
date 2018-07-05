import time

import telebot
import requests
import os
import psycopg2

port = int(os.environ.get('PORT', 5000))

token = "605519378:AAEd0WOYiatGI-Nrf9vK2DLgJdFVD2NpMZc"
bot = telebot.TeleBot(token)

con = psycopg2.connect("host='ec2-54-235-252-137.compute-1.amazonaws.com'dbname='db9rtffg17f3u2'user='qwcszqxjgxwgpe'password='2dcd995c072be1b1b4b3e3c4e6674629bf1cf8700dc26cad5ff0413194a9d07a'")
cursor = con.cursor()

#cursor.execute("DROP TABLE users") # удалить базу данных
#con.commit()
#cursor.execute("CREATE TABLE users (id varchar(60), mode varchar(20) )")
#con.commit()

@bot.message_handler(func=lambda msg: True)
def greeting(message):

    try:
        chat_id = str(message.chat.id)
        cursor.execute('SELECT * FROM users WHERE id=%s', (chat_id,))
        user = (cursor.fetchone())
    except:
        chat_id = '0'
        msg = 'error'
        user = '0'

    if user == None:

        cursor.execute("INSERT INTO users VALUES(%s,%s)",(chat_id,'own'))
        con.commit()

    try:

        text = message.text  # get user message

        if '/change_mode_chat' in text:

            cursor.execute('''UPDATE users SET mode = %s WHERE id = %s''', ('chat',chat_id,))
            con.commit()

            s = 'mode was changed'

        elif '/change_mode_own' in text:

            cursor.execute('''UPDATE users SET mode = %s WHERE id = %s''', ('own',chat_id))
            con.commit()

            s = 'mode was changed'

        elif text=='/start':

            s = 'Hello!\nExample of commands: btc usd, btc rur, zec usd'

        elif text == '/help':

            s = 'Hello!Example of commands: btc usd, btc rur, zec usd\nThis rates are from WEX.Change bot mode for chat: /change_mode_chat (and for own /change_bot_own)'

        else:
            pair = text.replace(" ", "_")  # replace to get pair
            url = 'https://wex.nz/api/3/ticker/' + pair  # send json request

            response = requests.get(url)
            list = (response.json()[pair])  # get list
            content = dict(list)  # convert to dictionary
            s = text + " - " + str(content["last"])  # print ["last"] price

    except:

        try:

            if user[1] == 'own':
                s = "Not valid pair( /help )"
            else:
                s = None

        except:
            s = None

    if s != None:

        bot.send_message(message.chat.id, s)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)

# ConnectionError and ReadTimeout because of possible timout of the requests library
# TypeError for moviepy errors
# maybe there are others, therefore Exception