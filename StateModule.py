#Список ошибок:
#   001 - неопределённый статус

import DataBaseWorker as DBW

#=============== States ==================
Normal = 0
AddIngridients = 1
AddDishes = 2
DishesIngridients = 3

State = Normal

#=============== Other ==================
WordsForState_Normal = [ 'отмена', 'нет']
WordsForState_AddIngridients = [
'добавить продукт',
'новый продукт',
'нет',
'да'
]
WordsForState_AddDishes = ['добавить блюдо']
WordsForState_DishesIngridients = ['блюдо']

#=============== Automat ================
def StateWork(message):
    global State
    message_text = message.lower()

    if State == Normal:
        if message_text in WordsForState_AddIngridients:
            ChangeBotState(AddIngridients)
            return 'Назови ингридиент'
        elif message_text in WordsForState_AddDishes:
            ChangeBotState(AddDishes)
            return 'Назови блюдо'
        elif message_text in WordsForState_DishesIngridients:
            ChangeBotState(DishesIngridients)
            return 'Напиши интересующий тебя ингридиент'
        else:
            return 'Неизвестная просьба'
    elif State == AddIngridients:
        if message_text in WordsForState_Normal:
            ChangeBotState(Normal)
            return "Буду ждать следующей команды"
        DBW.return_query_result(query_add_ingredients(), (message_text,))
        return 'Новый продукт добавлен, добавить ещё?'
        pass
    elif State == AddDishes:
        if message_text in WordsForState_Normal:
            ChangeBotState(Normal)
            return "Буду ждать следующей команды"
        pass
    elif State == DishesIngridients:
        if message_text in WordsForState_Normal:
            ChangeBotState(Normal)
            return "Буду ждать следующей команды"
        args = message_text.split(',')
        args = message_text.split(';')
        result = DBW.return_query_result(query_get_dishes(args))
        num = 1
        resultMessage = ''
        for element in result:
            resultMessage += str(num) + '. ' + str(element[0]) + '\n'
        return resultMessage + "\nНайти блюда для ещё одного ингридиента?"
    return "ОШИБКА №001.\nОбратитесь к разработчикам"

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

#=========== вспомогательные процедуры и функции ========================
def ChangeBotState(newState):
    global State
    if State == newState:
        return

    message = 'Статус бота изменился с [' + str(State) +'] '
    State = newState
    message += 'на [' + str(State) + ']'
    if State == newState:
        print(message)
        return True
    else:
        print(message + ' !!! СТАТУС БОТА НЕ СООТВЕТСВУЕТ НОВОМУ СТАТУСУ ПРИ ИЗМЕНЕНИИ В ФУНКЦИИ \'ChangeBotState()\'')
