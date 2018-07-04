import telebot
import json
import requests
import os

port = int(os.environ.get('PORT', 5000))

token = "595047320:AAGV1T9Dg0Y1RVzjqxmvLE4eYdI-XeAnjyY"
bot = telebot.TeleBot(token)

@bot.message_handler(func=lambda msg: True)
def greeting(message):
    try:
        text = message.text  # get user message

        pair = text.replace(" ", "_")  # replace to get pair
        url = 'https://wex.nz/api/3/ticker/' + pair  # send json request

        response = requests.get(url)
        list = (response.json()[pair])  # get list
        content = dict(list)  # convert to dictionary
        s = "Курс " + text + " - " + str(content["last"])  # print ["last"] price

    except KeyError:
        s = "Ошибка!Вы неправильно указали пару!"  # для использования в чатах убрать эту строчку

    bot.send_message(message.chat.id, s)

bot.polling()