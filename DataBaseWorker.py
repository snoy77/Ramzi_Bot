import mysql.connector
from mysql.connector import connect, Error
import TelegaInfo as TI



def return_query_result(query_to_bd, val = None):
    if not val == None:
        try:
            with connect(
                host = TI.DB_host,
                user = TI.DB_login,
                password = TI.DB_password,
                database = TI.DB_name,
            ) as connection:
                print("> Успешно: " + str(connection))
                with connection.cursor() as cursor:
                    print("> Запрос: \'" + query_to_bd + "\'...\nАргументы:" + str(val))
                    #Поулчаем резульатт по запросу
                    cursor.execute(query_to_bd, val)

                    connection.commit()
                    #перерабатываем ег ов список
                    result = cursor.fetchall()

                    print("> Успешно: " + str(cursor.rowcount) + " строк")
                    print("> Результат запроса:\n" + str(result))


                    if cursor.rowcount == 0:
                        return False
                    else:
                        return result
        except Error as e:
            print(str(e))
        return 404
    try:
        with connect(
            host = TI.DB_host,
            user = TI.DB_login,
            password = TI.DB_password,
            database = TI.DB_name,
        ) as connection:
            print("> Успешно: " + str(connection))
            with connection.cursor() as cursor:
                print("> Запрос: \'" + str(query_to_bd) + "\'...")
                #Поулчаем резульатт по запросу

                for query_text in query_to_bd.split(';'):
                    cursor.execute(query_text, multi=True)
                    print('>> ' + str(cursor))
        
                #перерабатываем ег ов список
                result = cursor.fetchall()
                print("> Успешно: " + str(cursor.rowcount) + " строк")
                print("> Результат запроса:\n" + str(result))


                if cursor.rowcount == 0:
                    return False
                else:
                    return result
    except Error as e:
        print(str(e))
    return 404
