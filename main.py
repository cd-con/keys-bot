import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_bot import VkBot
import settings as s


def write_msg(user_id, message):
    vk_api.VkApi(token=s.token).method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random.randint(0, 2048)})
try:
    longpoll = VkLongPoll(vk_api.VkApi(token=s.token))
except:
    exit('NullToken error: token is invalid')
print("Бот запущен")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            bot = VkBot(event.user_id)
            write_msg(event.user_id, bot.new_message(event.text, event.user_id))


