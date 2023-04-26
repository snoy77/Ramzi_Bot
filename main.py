import telebot
from telebot import types

import TelegaInfo as TI
import StateModule as SM

#Статус нынешней операции
#   *0 - начало работы, ожидание любого события
#   *1 - Ожидание названия материала для добавления его в БД
#   2 - Ожидание названия материала для удаления его в БД
#   *3 - Добавление продукта в список БД
#   4
#   5 - ожидание навзаний ингридиентов для получения имеющихся рецептов
#   6 - дать рецепты



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

    BotState_Need = SM.CheckState(message_text)
    SM.ChangeBotState(BotState_Need)
    going_message = SM.doState(message_text)

    bot.send_message(chat_id, going_message)

print('Работа бота...\n')
bot.polling(none_stop=True, interval=0)
print('\n\nРабота бота ЗАВЕРШЕНА')
