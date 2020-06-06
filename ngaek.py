import vk
import telebot
import urllib.request
import time
import configparser
import traceback

def update_last_id(section, setting, value):
    config = configparser.ConfigParser()
    config.read("./ngaek.ini")
    config.set(section, setting, value)
    with open("./ngaek.ini", "w") as config_file:
        config.write(config_file)


def get_last_post(section, setting):
    config = configparser.ConfigParser()
    config.read("./ngaek.ini")
    last_id = config.get(section, setting)
    return last_id


if __name__ == "__main__":
    while 1:
        try:
            bot = telebot.TeleBot('1175875986:AAHLQgN7qPfiJShormK-bhScNnbrdSvwMvo')
            api = vk.API(vk.Session('7e9d1f397e9d1f397e9d1f392d7eef6cc877e9d7e9d1f3920462541c9f013a06b72234a'))
            while 1:
                last_id = get_last_post("POST", "ID_LAST_POST")
                post = api.wall.get(owner_id= -40400418, domain= 'https://vk.com/public40400418', count= 1, v= 5.103)['items'][0]
                print(post)
                if post['text'] == '':
                    if len(post['attachments']) == 1:
                        if int(last_id) != int(post['id']):
                            img_url = post['attachments'][-1]['photo']['sizes'][-1]['url']
                            urllib.request.urlretrieve(img_url, './ngaek.jpg')
                            image = open('./ngaek.jpg', 'rb')
                            bot.send_photo(chat_id= '@ngaek2', photo= image)
                            update_last_id("POST", "ID_LAST_POST", str(post['id']))
                time.sleep(15)
        except:
            print(traceback.format_exc())
            