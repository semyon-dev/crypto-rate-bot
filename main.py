import telebot
import requests
import os
import psycopg2

port = int(os.environ.get('PORT', 5000))

token = "605519378:AAEd0WOYiatGI-Nrf9vK2DLgJdFVD2NpMZc"
bot = telebot.TeleBot(token)

con = psycopg2.connect("host='ec2-54-235-252-137.compute-1.amazonaws.com'dbname='db9rtffg17f3u2'user='qwcszqxjgxwgpe'password='2dcd995c072be1b1b4b3e3c4e6674629bf1cf8700dc26cad5ff0413194a9d07a'")
cursor = con.cursor()

#cursor.execute("CREATE TABLE users (id int, mode varchar(10) )")

#cursor.execute("DROP TABLE <name of table>") # удалить базу данных

@bot.message_handler(func=lambda msg: True)
def greeting(message):

    cursor.execute('SELECT * FROM users WHERE id=%s', (message.chat.id,))
    user = (cursor.fetchone())

    if user == None:

        cursor.execute("INSERT INTO users VALUES(%s,%s)",(message.chat.id,'own'))
        con.commit()

    try:
        text = message.text  # get user message

        if '/change_mode_chat' in text:

            cursor.execute('''UPDATE users SET mode = %s WHERE id = %s''', ('chat', message.chat.id))
            con.commit()

            s='режим успешно изменен'

        elif '/change_mode_own' in text:

            cursor.execute('''UPDATE users SET mode = %s WHERE id = %s''', ('own', message.chat.id ))
            con.commit()

            s = 'Режим успешно изменен'

        else:
            pair = text.replace(" ", "_")  # replace to get pair
            url = 'https://wex.nz/api/3/ticker/' + pair  # send json request

            response = requests.get(url)
            list = (response.json()[pair])  # get list
            content = dict(list)  # convert to dictionary
            s = "Курс " + text + " - " + str(content["last"])  # print ["last"] price

    except KeyError:

        if user[1] == 'own':
            s = "Ошибка!Вы неправильно указали пару!"
        else:
            s=None

    if s!=None:

        bot.send_message(message.chat.id, s)

bot.polling()