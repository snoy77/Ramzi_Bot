import telebot
from telebot import types

import TelegaInfo as TI
import StateModule as SM

#----------------Определение некоторых методов----------------
def getMessageChatMainInfo(chat):
    return str(chat.id) + ' ' + str(chat.username) + ' ' + str(chat.title)
def getMessageUserMainInfo(user):
    return str(user.id) + ' ' + str(user.first_name) + ' ' + str(user.last_name)






bot = telebot.TeleBot(TI.token)

@bot.message_handler(content_types=['text'])
def message_going(message):


    chat_id = message.chat.id
    message_text = message.text
    message_data = message.date
    message_user = getMessageUserMainInfo(message.from_user)
    message_chat = getMessageChatMainInfo(message.chat)

    #BotState_Need = SM.CheckState(message_text)
    #SM.ChangeBotState(BotState_Need)
    #going_message = SM.doState(message_text)
    going_message = SM.StateWork(message_text)

    bot.send_message(chat_id, going_message)

while True:
    print('Работа бота...\n')
    try:
        bot.polling(none_stop=True, interval=0)
    except ZeroDivisionError as err:
        print('\n\nАварийное выключение бота:\n\n')
    print('\n\nРабота бота ЗАВЕРШЕНА')
