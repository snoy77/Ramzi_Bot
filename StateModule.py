import DataBaseWorker as DBW

WordsForState_0 = [ 'отмена', 'нет']
StateForState_0 = [1]

WordsForState_1 = [
'добавить продукт',
'новый продукт',
'нет',
'да'
]
StateForState_1 = [0, 1]
StateForState_3 = [3]

WordsForState_5 = ['блюдо']
StateForState_5 = [0]
StateForState_6 = [5]
BotState = 0

#====== Check state ===================
def CheckState_0(message_text, BotStateNow):
    return message_text in WordsForState_0 and BotStateNow in StateForState_0
def CheckState_1(message_text, BotStateNow):
    return message_text in WordsForState_1 and BotStateNow in StateForState_1
def CheckState_3(message_text, BotStateNow):
    return BotStateNow == 1 and (message_text != 'да' or message_text != 'нет')
def CheckState_5(message_text, BotStateNow):
    return message_text in WordsForState_5 and BotStateNow in StateForState_5
def CheckState_6(message_text, BotStateNow):
    return BotStateNow == 5 and (message_text != 'да' or message_text != 'нет')

def CheckState(message_text):
    global BotState
    if CheckState_0(message_text, BotState):
        return 0
    elif CheckState_1(message_text, BotState):
        return 1
    elif CheckState_3(message_text, BotState):
        return 3
    elif CheckState_5(message_text, BotState):
        return 5
    elif CheckState_6(message_text, BotState):
        return 6
    else:
        return BotState

#=========== Do state ================
def doState_0(message_text):
    return 'Ожидаю команды...'
def doState_1(message_text):
    return 'Назови продукт, пожалуйста'
def doState_3(message_text):
    DBW.return_query_result(query_add_ingredients(), (message_text,))
    ChangeBotState(1)
    return 'Новый продукт добавлен, добавить ещё?'
def doState_5(message_text):
    return 'Напиши интересующий тебя ингридиент'
def doState_6(message_text):
    args = message_text.split(',')
    args = message_text.split(';')
    result = DBW.return_query_result(query_get_dishes(args))
    num = 1
    resultMessage = ''
    for element in result:
        resultMessage += str(num) + '. ' + str(element[0]) + '\n'

    ChangeBotState(5)
    return resultMessage


def doState(message_text):
    global BotState
    if BotState == 0:
        return doState_0(message_text)
    elif BotState == 1:
        return doState_1(message_text)
    elif BotState == 3:
        return doState_3(message_text)
    elif BotState == 5:
        return doState_5(message_text)
    elif BotState == 6:
        return doState_6(message_text)


#========================
def ChangeBotState(newState):
    global BotState
    if BotState == newState:
        return

    message = 'Статус бота изменился с [' + str(BotState) +'] '
    BotState = newState
    message += 'на [' + str(BotState) + ']'
    if BotState == newState:
        print(message)
        return True
    else:
        print(message + ' !!! СТАТУС БОТА НЕ СООТВЕТСВУЕТ НОВОМУ СТАТУСУ ПРИ ИЗМЕНЕНИИ В ФУНКЦИИ \'ChangeBotState()\'')


#====== ЗАПРОСЫ ==========
def query_add_ingredients():
    query_to_bd = "insert into ingredients (name) values (%s)"
    return query_to_bd
def query_get_dishes(args):

    query_to_bd = "CREATE TEMPORARY TABLE `need_ingredients` SELECT id FROM `ingredients` WHERE name IN ("
    query_to_bd += "\'\'"
    for el in args:
        query_to_bd += ",\'" + el + "\'"

    query_to_bd += "); CREATE TEMPORARY TABLE `TT_dishes` SELECT dishes_ingredients.id_dishes FROM `dishes_ingredients` INNER JOIN `need_ingredients` ON dishes_ingredients.id_ingredients = need_ingredients.id; SELECT dishes.name FROM `dishes` INNER JOIN `TT_dishes` ON dishes.id = TT_dishes.id_dishes"
    return query_to_bd.replace('`', '')
