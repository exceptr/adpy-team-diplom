from pprint import pprint
import vk_api
from LiteVkApi import Client, Keyboard, Button
from vk_api.longpoll import VkEventType
from vk_api.tools import VkTools
from vk_api.execute import VkFunction
from random import randrange


def run_bot():
    token_group = "9408bb531621ecadc532e2756e8e7034130b7ace7f7551351bbeac71b0342226cd5c1e6dff04f7b543d14"
    session_group = vk_api.VkApi(token=token_group)
    vk_group = session_group.get_api()
    vk_session = Client.give_session(session_group)
    keyboard = Keyboard(True, False,
                        [[Button.text("Да", "зеленый"), Button.text("Нет", "белый")],
                         [Button.url("Кнопка3url", "https://vk.com/")]])
    waiting_url_users = set()
    while True:
        # if event.type == VkEventType.MESSAGE_NEW \
        #         and event.user_id in waiting_url_users \
        #         and event.text:
        #     advert = event.text
        #     waiting_url_users.remove(event.user_id)
        if vk_session.check_new_msg():
            event = vk_session.get_event()
            eventxt, userid = event.text, event.user_id
            if eventxt.lower() == 'привет':
                vk_session.msg(f'Привет. Вас интересует поиск людей по критериям ?', userid)
                vk_session.send_keyboard(keyboard, event.user_id, 'Ответ "Да" для продолжения\n'
                                                                  'Ответ "Нет" для завершения')
            elif eventxt.lower() == 'да':
                vk_session.msg(f'Укажите возраст от', userid)
            elif eventxt.lower() == 'поиск':
                people_info = get_people_by_parameters(18, 25, 1, "Москва")
                print(people_info)
                if people_info is None:
                    vk_session.msg(f'Профиль удалён или заблокирован, перейдите к следующему варианту', userid)
                elif len(people_info) == 6:
                    first_name = people_info['first_name']
                    last_name = people_info['last_name']
                    link_people = people_info['link_people']
                    photos = people_info['photos']
                # print(len(people_info))
                    vk_session.msg(f'{first_name} {last_name}\n{link_people}', userid)
                    # photos = people_info['photos']
                    vk_group.messages.send(attachment=photos, user_id=userid, random_id=randrange(10 ** 7))
                    # for event_txt in photos:
                    #     # vk_session.msg(f'Привет, {userid}', userid)
                    #     vk_group.messages.send(attachment=event_txt, user_id=userid, random_id=randrange(10 ** 7))
                elif len(people_info) == 5:
                    first_name = people_info['first_name']
                    last_name = people_info['last_name']
                    link_people = people_info['link_people']
                    vk_session.msg(f'{first_name} {last_name}\n{link_people}\nЗакрытый профиль', userid)
            elif eventxt == 'Как дела?':
                vk_session.msg('Хорошо, а у тебя?', userid)


token_user = "a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd"
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
        # pprint(i)
        # print(i['is_closed'])
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
    'counter': 14
}


def increase_counter():
    counter_offset['counter'] += 1
    return counter_offset['counter']



if __name__ == '__main__':
    run_bot()
    # get_people_by_parameters(18, 25, 1, "Москва")
    # get_popular_photos()
    # increase_counter()
    # increase_counter()
    # increase_counter()
    # print(counter_offset)