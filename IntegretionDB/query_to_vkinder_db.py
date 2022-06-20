from Connect import connection
from psycopg2 import Error


# регистрация пользователя в БД
def insert_data_userid(vk_id):
    try:
        cursor = connection.cursor()
        insert_query = f"Insert into vkuser(vk_id) values ({vk_id});"
        cursor.execute(insert_query, vk_id)
        connection.commit()
        count = cursor.rowcount
        print('Запись добавлена', count)
    except(Exception, Error) as error:
        print('Возникла ошибка при добавлении:', error)


# добавить в таблицу избранного
def insert_data_favorite(favorite_link):
    try:
        cursor = connection.cursor()
        insert_query = f"Insert into Favorite(favorite_link) values ('{favorite_link}');"
        cursor.execute(insert_query, favorite_link)
        connection.commit()
        count = cursor.rowcount
        print('Запись добавлена', count)
    except(Exception, Error) as error:
        print('Возникла ошибка при добавлении:', error)
#
# def insert_data_city(city):

# добавить отношение юзера к избранному
def insert_data_VKUserFavorite(id_user, id_favorite):
    try:
        cursor = connection.cursor()
        insert_query = f"Insert into VKUserFavorite(id_user, id_favorite)" \
                       f" values ({id_user}, {id_favorite});"
        cursor.execute(insert_query, id_user)
        connection.commit()
        count = cursor.rowcount
        print('Запись добавлена', count)
    except(Exception, Error) as error:
        print('Возникла ошибка при добавлении:', error)


# добавить info о пользователе в БД
def insert_query_userinfo(age, status, gender):
    try:
        cursor = connection.cursor()
        query_userinfo = f"Insert into UserInfo(age, family_status, gender) values ({age}, {status}, {gender});"
        cursor.execute(query_userinfo)
        connection.commit()
        count = cursor.rowcount
        print('Запись добавлена', count)
    except(Exception, Error) as error:
        print('Возникла ошибка при добавлении:', error)


# проверка id в базе
def select_query_vkuser():
    cursor = connection.cursor()
    query_vkuser = "Select * from vkuser"
    cursor.execute(query_vkuser)
    vkuser_records = cursor.fetchall()
    res = []
    for i in vkuser_records:
        res += [item for item in i]
    return res
# print(select_query_vkuser())


def select_vkuser_id(vk_id):
    cursor = connection.cursor()
    query_vkuser = f"Select id from VKUser" \
                   f" Where vk_id = {vk_id}"
    cursor.execute(query_vkuser)
    vkuser_records = cursor.fetchall()
    res = []
    for i in vkuser_records:
        res += [item for item in i]
        for id_ref in res:
            return id_ref
# print(select_vkuser_id('144344533'))


def select_favorite_id():
    cursor = connection.cursor()
    query_vkuser = f"Select id from Favorite"
    cursor.execute(query_vkuser)
    vkuser_records = cursor.fetchall()
    res = []
    for i in vkuser_records:
        res += [item for item in i]
    return res[-1]


# показать список избранного
def select_favorite(vk_id):
    cursor = connection.cursor()
    query_favorite = f"Select favorite_link From Favorite " \
                     f"Join VKUserFavorite vf on Favorite.id = vf.id_favorite " \
                     f"Join vkuser u on u.id = vf.id_user " \
                     f"Where u.vk_id = {vk_id};"
    cursor.execute(query_favorite)
    favorite_records = cursor.fetchall()
    new_list =[]
    for link in favorite_records:
        new_list += [item for item in link]
        res = '\n'.join(new_list)
    return res


def stop_connect():
    cursor = connection.cursor()
    cursor.close()
    connection.close()
    print("Соединение с PostgresSQL закрыто")
