import requests, json, telebot, sqlite3, datetime, random

msg_time = datetime.datetime.now()

# функция отправки гифок
def get_gif():
    apikey = "AIzaSyBwv8XCvtCEtQeO9abvAAt3vurAcNC8YgM"
    response = requests.get(f"https://tenor.googleapis.com/v2/search?q=touhou&key={apikey}&random=true&media_filter=gif&limit=1")
    gif_data = json.loads(response.text)
    return gif_data["results"][0]['media_formats']["gif"]["url"]

# функция отправки новостей
def get_news():
    global msg_time
    if (datetime.datetime.now() - msg_time).seconds < 10:
        return "В Генсокё всё по-старому"
    else:
        con = sqlite3.connect("db_4_indv_project.db")
        cursor = con.cursor()
        cursor.execute('SELECT desc FROM news WHERE id=?', (random.randint(1, 6), ))
        news = cursor.fetchone()
        msg_time = datetime.datetime.now()
        return news[0]

bot = telebot.TeleBot("8181972121:AAG1cSkgwIRlQAwiiWed4hMHaN5e-iFj9DM")

# превед
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """ВЕЛИКАЯ, НЕПОВТОРИМАЯ И ОПРЕДЕЛЁННО ТОЧНО НЕ БАКА, СЫРНО, ПРИВЕТСТВУЕТ ТЕБЯ
Чё тебе надо от меня, а? Не знаешь? Дык пропиши /help и будет тебе всё предельно чечётка и ясно, что тебе от меня нужно
""")

# хелпа
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, """ВЕЛИКАЯ, НЕПОВТОРИМАЯ И ОПРЕДЕЛЁННО ТОЧНО НЕ БАКА, СЫРНО, МОЖЕТ СДЕЛАТЬ ДЛЯ ТЕБЯ СЛЕДУЮЩЕЕ:
/gifka - отправить тохо-гифку
/news - рассказать последние новости в Генсокё
НИ В КОЕМ СЛУЧАЕ НЕ НАЗЫВАЙ МЕНЯ "БАКА"!!!""")

# гиф
@bot.message_handler(commands=['gifka'])
def send_gif(message):
    bot.send_message(message.chat.id, get_gif())

# новости
@bot.message_handler(commands=['news'])
def send_news(message):
    bot.send_message(message.chat.id, get_news())

bot.infinity_polling()