import vk_api
import urllib.request
import random
import json
from vk_api.longpoll import VkLongPoll, VkEventType

token = '1345ec093dca7f163cd2058b366589a18d2caf27e16555f776dc8c86fd9cafad14bca908956e6a729696c'


def isOnline(uid):
    a = urllib.request.urlopen("https://api.vk.com/method/users.get?user_id={i}&fields=online&access_token={t}&v=5.131".format(i=uid, t=token)).read()
    print(a)
    try:
        b = int(json.loads(a)['response'][0]['online'])
    except ValueError:
        b = -1
    return b


maxint = 2147483647
vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if event.from_user:
            userId = event.text
            outText = ''
            onl = isOnline(userId)
            if onl == 1:
                outText = "online"
            elif onl == 0:
                outText = "offline"
            else:
                outText = "неверный ID"
            vk.messages.send(user_id=event.user_id, message=outText, random_id=random.randint(0, maxint))
