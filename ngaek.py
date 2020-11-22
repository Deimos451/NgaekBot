import vk
import telebot
import urllib.request
import time, datetime
import psycopg2
import traceback
import os

DATABASE_URL = os.environ['DATABASE_URL']
TELEBOT_TOKEN = os.environ['TELEBOT_TOKEN']
VK_TOKEN = os.environ['VK_TOKEN']

connection = psycopg2.connect(DATABASE_URL, sslmode='require')


def update_last_post_unix(value):
    cursor = connection.cursor()
    cursor.execute("UPDATE post_id SET last_post_unix = (%s)", [value])
    connection.commit()


def get_last_post_unix():
    cursor = connection.cursor()
    cursor.execute("SELECT last_post_unix FROM post_id LIMIT 1")
    last_id = cursor.fetchall()[0][0]
    return last_id


if __name__ == "__main__":
    while 1:
        try:
            bot = telebot.TeleBot(TELEBOT_TOKEN)
            api = vk.API(vk.Session(VK_TOKEN))
            while 1:
                try:
                    last_id = get_last_post_unix()
                    post = api.wall.get(owner_id= -40400418, domain= 'https://vk.com/public40400418', count= 1, v= 5.103)['items'][0]
                    if (post['date'] > get_last_post_unix()) and ((post['text'] == '') or ('UPD' in post['text'])) and (len(post['attachments']) == 1):
                        img_url = post['attachments'][-1]['photo']['sizes'][-1]['url']
                        urllib.request.urlretrieve(img_url, './ngaek.jpg') 
                        image = open('./ngaek.jpg', 'rb')
                        bot.send_photo(chat_id= '@ngaek2', photo= image)
                        update_last_post_unix(post['date'])
                    time.sleep(60)
                except:
                    print(traceback.format_exc())
                    time.sleep(120)
        except:
            print(traceback.format_exc())
            time.sleep(15)
    