import vk
import telebot
import urllib.request
import time
import psycopg2
import traceback

DATABASE_URL = os.environ['DATABASE_URL']
connection = psycopg2.connect(DATABASE_URL, sslmode='require')

''' connection = psycopg2.connect(  dbname=     'de02gtvjqfnkg8', 
                                host=       'ec2-52-208-175-161.eu-west-1.compute.amazonaws.com',
                                user=       'qkiuqhynexpjrm', 
                                password=   '9967fb4461bc54df58673a08020f2fe5234f897159dbb0234a12380b1f5c382b', 
                                port=       '5432') '''


def update_last_id(value):
    cursor = connection.cursor()
    cursor.execute("UPDATE post_id SET last_post = (%s)", [value])
    connection.commit()

def get_last_post():
    cursor = connection.cursor()
    cursor.execute("SELECT last_post FROM post_id LIMIT 1")
    last_id = cursor.fetchall()[0][0]
    return last_id


if __name__ == "__main__":
    while 1:
        try:
            bot = telebot.TeleBot('1175875986:AAHLQgN7qPfiJShormK-bhScNnbrdSvwMvo')
            api = vk.API(vk.Session('51f237fc51f237fc51f237fc97518049f2551f251f237fc0f2fe2db99886533b296dba1'))
            while 1:
                try:
                    last_id = get_last_post()
                    post = api.wall.get(owner_id= -40400418, domain= 'https://vk.com/public40400418', count= 1, v= 5.103)['items'][0]
                    update_last_id(post['id'])
                    if post['text'] == '':
                        if len(post['attachments']) == 1:
                            if int(last_id) != int(post['id']):
                                img_url = post['attachments'][-1]['photo']['sizes'][-1]['url']
                                urllib.request.urlretrieve(img_url, './ngaek.jpg') 
                                image = open('./ngaek.jpg', 'rb')
                                bot.send_photo(chat_id= '@ngaek2', photo= image)
                    time.sleep(60)
                except:
                    print(traceback.format_exc())
                    time.sleep(120)
        except:
            time.sleep(15)
    