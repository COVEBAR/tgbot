import requests, json, telebot
# функция отправки гифок
def get_gif():
    apikey = "AIzaSyBwv8XCvtCEtQeO9abvAAt3vurAcNC8YgM"
    response = requests.get(f"https://tenor.googleapis.com/v2/search?q=touhou&key={apikey}&random=true&media_filter=gif&limit=1")
    gif_data = json.loads(response.text)
    return gif_data["results"][0]['media_formats']["gif"]["url"]


bot = telebot.TeleBot("8181972121:AAG1cSkgwIRlQAwiiWed4hMHaN5e-iFj9DM")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """ВЕЛИКАЯ, НЕПОВТОРИМАЯ И ОПРЕДЕЛЁННО ТОЧНО НЕ БАКА, СЫРНО, ПРИВЕТСТВУЕТ ТЕБЯ
Чё тебе надо от меня, а?
""")

@bot.message_handler(commands=['gifka'])
def send_gif(message):
    bot.send_message(message.chat.id, get_gif())

bot.infinity_polling()