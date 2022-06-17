from pprint import pprint
import vk_api
from LiteVkApi import Client, Keyboard, Button
from random import randrange
from tokens import GROUP_TOKEN, USER_TOKEN


def run_bot():
    token_group = GROUP_TOKEN
    session_group = vk_api.VkApi(token=token_group)
    vk_group = session_group.get_api()
    vk_session = Client.give_session(session_group)
    keyboard = Keyboard(True, False,
                        [[Button.text("Да", "зеленый"), Button.text("Нет", "белый")],
                         [Button.text("Поиск", "синий")],
                         [Button.text("В избранное", "белый"), Button.text("Показать избранное", "белый")]])
    key_word = ['поиск', 'старт', 'в избранное', 'показать избранное', 'стоп', 'да', 'нет', 'привет']
    search_param = {}
    last_search_people_info = {}
    while True:
        if vk_session.check_new_msg():
            event = vk_session.get_event()
            eventxt, userid = event.text, event.user_id
            if eventxt.lower() == 'привет':
                vk_session.msg(f'Привет. Вас интересует поиск людей по критериям ?', userid)
                vk_session.send_keyboard(keyboard, event.user_id, 'Кнопка "Да" для продолжения\n'
                                                                  'Кнопка "Нет" для завершения')
            # Поиск пары по критериям
            if eventxt.lower() == 'да':
                vk_session.msg(f'Для поиска введите параметры, пример - девушка 18-39 город', userid)
            if eventxt.lower() not in key_word and len(eventxt) > 1:
                try:
                    print(eventxt.lower())
                    sex = 0
                    search_param['sex'] = sex
                    if eventxt[0:7].lower() == 'девушка':
                        sex = 1
                        search_param['sex'] = sex
                    elif eventxt[0:7].lower() == 'мужчина':
                        sex = 2
                        search_param['sex'] = sex
                    age_from = int(eventxt[8:10])
                    age_to = int(eventxt[11:14])
                    hometown = eventxt[14:len(eventxt)].lower()
                    search_param['age_from'] = age_from
                    search_param['age_to'] = age_to
                    search_param['hometown'] = hometown
                    search_param['id'] = userid
                    vk_session.msg(f'Для поиска нажмите кнопку "Поиск"', userid)
                except ValueError:
                        vk_session.msg(f'Некорректно введены параметры, укажите параметры поиска в формате - '
                                       f'девушка 18-39 город', userid)
            if eventxt.lower() == 'поиск':
                people_info = get_people_by_parameters(search_param['age_from'], search_param['age_to'],
                                                       search_param['sex'], search_param['hometown'])
                if people_info is None:
                    vk_session.msg(f'Профиль удалён или заблокирован, перейдите к следующему варианту', userid)
                elif len(people_info) == 6:
                    first_name = people_info['first_name']
                    last_name = people_info['last_name']
                    link_people = people_info['link_people']
                    last_search_people_info.update(first_name=first_name)
                    last_search_people_info.update(last_name=last_name)
                    last_search_people_info.update(link_people=link_people)
                    photos = people_info['photos']
                    vk_session.msg(f'{first_name} {last_name}\n{link_people}', userid)
                    vk_group.messages.send(attachment=photos, user_id=userid, random_id=randrange(10 ** 7))
                elif len(people_info) == 5:
                    first_name = people_info['first_name']
                    last_name = people_info['last_name']
                    link_people = people_info['link_people']
                    last_search_people_info.update(first_name=first_name)
                    last_search_people_info.update(last_name=last_name)
                    last_search_people_info.update(link_people=link_people)
                    vk_session.msg(f'{first_name} {last_name}\n{link_people}\nЗакрытый профиль', userid)
            # Когда нажимаем кнопку в избранное, добавляем послнеднего кого искали в избранное
            if eventxt.lower() == 'в избранное':
                print(last_search_people_info)
            # Здесь нужно вытащить из БД всех пользователей который добавили в избранное
            if eventxt.lower() == 'показать избранное':
                ...


token_user = USER_TOKEN
session_user = vk_api.VkApi(token=token_user)
vk_user = session_user.get_api()


def get_people_by_parameters(age_from=None, age_to=None, sex=None, hometown=str, status=6, has_photo=1, count=1,
                             fields='boolean'):
    counter = increase_counter()
    response = vk_user.users.search(age_from=age_from, age_to=age_to, sex=sex, hometown=hometown, status=status,
                                    has_photo=has_photo, offset=counter, count=count, fields=fields)
    pprint(response)
    people_info = {}
    for i in response['items']:
        if i['is_closed'] == bool(True):
            counter = increase_counter()
            response = vk_user.users.search(age_from=age_from, age_to=age_to, sex=sex, hometown=hometown, status=status,
                                            has_photo=has_photo, offset=counter, count=count, fields=fields)
            for i in response['items']:
                people_info.update(id=i['id'])
                people_info.update(first_name=i['first_name'])
                people_info.update(last_name=i['last_name'])
                people_info.update(link_people=f"https://vk.com/id{str(i['id'])}")
                people_info.update(counter=counter)
                pprint(people_info)
                return people_info

        elif i['is_closed'] == bool(False):
            people_info.update(id=i['id'])
            people_info.update(first_name=i['first_name'])
            people_info.update(last_name=i['last_name'])
            people_info.update(link_people=f"https://vk.com/id{str(i['id'])}")
            people_info.update(counter=counter)
            id = people_info['id']
            response2 = vk_user.photos.getAll(owner_id=id, extended=1)
            photos = response2['items']
            photos_dict = {}
            for v in photos:
                attachment_photo = 'photo' + str(v['owner_id']) + '_' + str(v['id'])
                photos_dict[attachment_photo] = v['likes']['count']
                sorted_dict = sorted(photos_dict, key=photos_dict.__getitem__)
                popular_photos = sorted_dict[-3:]
                people_info.update(photos=popular_photos)
            pprint(people_info)
            return people_info


counter_offset = {
    'counter': 1
}


def increase_counter():
    counter_offset['counter'] += 1
    return counter_offset['counter']