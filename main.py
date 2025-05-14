import requests, json, telebot, sqlite3, datetime, randomadd

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

def math_game():
    problem = random.randint(0, 3)
    if problem == 0:
        num1 = random.randint(0, 100)
        num2 = random.randint(0, 100)
        problem = f"{num1} + {num2}"
        sol = num1 + num2
    elif problem == 1:
        num1 = random.randint(0, 30)
        num2 = random.randint(0, 30)
        problem = f"{num1} * {num2}"
        sol = num1 * num2
    elif problem == 2:
        num2 = random.randint(1, 50)
        num1 = num2 * random.randint(1, 10)
        problem = f"{num1} / {num2}"
        sol = num1 // num2
    elif problem == 3:
        num1 = random.randint(0, 100)
        num2 = random.randint(0, 99)
        while num2 > num1:
            num2 = random.randint(0, 99)
        problem = f"{num1} - {num2}"
        sol = num1 - num2

    wrong = random.randint(0, 100)
    while wrong == sol:
        wrong = random.randint(0, 100)
    return (problem, sol, wrong)


#тг бот
bot = telebot.TeleBot("8181972121:AAG1cSkgwIRlQAwiiWed4hMHaN5e-iFj9DM")

# превед
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"""ВЕЛИКАЯ, НЕПОВТОРИМАЯ И ОПРЕДЕЛЁННО ТОЧНО НЕ БАКА, СЫРНО, ПРИВЕТСТВУЕТ ТЕБЯ, "{message.chat.username}"
Чё тебе надо от меня, а? Не знаешь? Дык пропиши /help и будет тебе всё предельно чечётка и ясно, что тебе от меня нужно
""")

# хелпа
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, """ВЕЛИКАЯ, НЕПОВТОРИМАЯ И ОПРЕДЕЛЁННО ТОЧНО НЕ БАКА, СЫРНО, МОЖЕТ СДЕЛАТЬ ДЛЯ ТЕБЯ СЛЕДУЮЩЕЕ:
/gifka - отправить тохо-гифку
/news - рассказать последние новости в Генсокё
/math - задать математический пример
НИ В КОЕМ СЛУЧАЕ НЕ НАЗЫВАЙ МЕНЯ "БАКА"!!!""")

# гиф
@bot.message_handler(commands=['gifka'])
def send_gif(message):
    bot.send_message(message.chat.id, get_gif())

# новости
@bot.message_handler(commands=['news'])
def send_news(message):
    bot.send_message(message.chat.id, get_news())

#матеша
@bot.message_handler(commands=['math'])
def math(message):
    # создаём задачку и ответы - правильный (неправильный) и рандомный неправильный (правильный)
    problem, f_solution, r_solution = math_game()

    if random.randint(0, 1) == 1:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(f'{f_solution}', callback_data="fs"))
        markup.add(telebot.types.InlineKeyboardButton(f'{r_solution}', callback_data="ts"))
        bot.send_message(message.chat.id, f"""Вот тебе пример, который ты никогда не сможешь правильно решить:
{problem}""", reply_markup=markup)
    else:
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(f'{r_solution}', callback_data="ts"))
        markup.add(telebot.types.InlineKeyboardButton(f'{f_solution}', callback_data="fs"))
        bot.send_message(message.chat.id, f"""Вот тебе пример, который ты никогда не сможешь правильно решить:
{problem}""", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def math_check(callback):
    if callback.data == "fs":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Ха-ха-ха! Я же говорила, что ты никогда не сможешь его правильно решить! БАКА!")
    elif callback.data == "ts":
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Уф, а ты куда умнее, чем я изначально думала...")

# реакт на "бака"
@bot.message_handler()
def baka_check_status(message):
    if "бака" in message.text.lower() or "baka" in message.text.lower():
        bot.send_message(message.chat.id, """ВООБЩЕ-ТО Я ОЧЕНЬ УМНАЯ! ДА ТЫ САМ БАКА! ЧТО ВООБЩЕ ЗА ЧЕПУХУ ТЫ ГОРОДИШЬ ПРО МЕНЯ!""")

bot.infinity_polling()