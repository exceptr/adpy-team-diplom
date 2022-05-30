from pprint import pprint
import vk_api
from LiteVkApi import Client
from vk_api.tools import VkTools
from vk_api.execute import VkFunction

token_group = "9408bb531621ecadc532e2756e8e7034130b7ace7f7551351bbeac71b0342226cd5c1e6dff04f7b543d14"
session_group = vk_api.VkApi(token=token_group)
vk_group = session_group.get_api()

# vk_session = Client.give_session(session)
# while True:
#     if vk_session.check_new_msg():
#         event = vk_session.get_event()
#         eventxt, userid = event.text, event.user_id
#         if eventxt == 'Привет':
#             vk_session.msg(f'Привет, {userid}', userid)
#         elif eventxt == 'Как дела?':
#             vk_session.msg('Хорошо, а у тебя?', userid)

token_user = "a67f00c673c3d4b12800dd0ba29579ec56d804f3c5f3bbcef5328d4b3981fa5987b951cf2c8d8b24b9abd"
session_user = vk_api.VkApi(token=token_user)
vk_user = session_user.get_api()


def get_people_by_parameters(age_from=None, age_to=None, sex=None, hometown=str, status=6, has_photo=1, count=1):
    response = vk_user.users.search(age_from=age_from, age_to=age_to, sex=sex, hometown=hometown, status=status,
                                    has_photo=has_photo, count=count)
    photos_dict = {}
    for i in response['items']:
        people = response['items']
        response2 = vk_user.photos.getAll(owner_id=i['id'], extended=1)
        # pprint(response2['items'])
        photos = response2['items']
        for v in photos:
            # pprint(v['likes']['count'])
            # pprint(v['sizes'][-1])
            photos_dict[v['sizes'][-1]['url']] = v['likes']['count']
            # print(url_photo)
    pprint(photos_dict)


pprint(get_people_by_parameters(18, 25, 1, "Волжск"))
