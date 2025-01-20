import random
import time
import threading
from telebot import TeleBot

bot = TeleBot('7733062260:AAEUhtZt2I-okyVefvyYMl7xvzgMTh4qyQ0')
data = ["загрязнение", "стекло", "мусор", "завод", "выхлоп", "выбросы", "химия", "нефть", "газы", "климат", "потепление", "углерод", "фактор", "ущерб", "огонь", "пламя", "наводнение", "почва", "воздух", "диоксид", "атмосфера", "поражение"]

registered_users = {}  
user_scores = {}  
current_word = {}  
timer_thread = {}  

def shuffle_word(word):
    word_list = list(word)
    random.shuffle(word_list)
    return ''.join(word_list)

def start_timer(chat_id):
    time.sleep(45)  
    if chat_id in current_word:  
        user_scores[chat_id] -= 2  
        bot.send_message(chat_id, "Время вышло! У вас отняли 2 очка. Следующее слово...")
        send_new_word(chat_id)

def send_new_word(chat_id):
    if data:  
        word = random.choice(data)
        shuffled = shuffle_word(word)
        current_word[chat_id] = word
        bot.send_message(chat_id, f"{registered_users[chat_id]}, угадай слово: {shuffled}")
        timer_thread[chat_id] = threading.Thread(target=start_timer, args=(chat_id,))
        timer_thread[chat_id].start()  
    else:
        bot.send_message(chat_id, "Поздравляю! Вы угадали все слова! 🎉")

@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id not in registered_users:
        bot.send_message(message.chat.id, "Сначала зарегистрируйтесь с помощью команды /register.")
        return
    user_scores[message.chat.id] = 10
    send_new_word(message.chat.id)

@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = (
        "Я игровой бот! Вот что вы можете делать:\n"
        "/start - Начать игру и угадать слово\n"
        "/help - Получить помощь и информацию о командах\n"
        "/github - Мой GitHub\n"
        "/register - Зарегистрироваться для участия в игре\n"
        "/exit - Выйти из игры и посмотреть свои очки\n"
        "Просто напишите слово, которое, по вашему мнению, является правильным ответом, и я скажу, правы ли вы!"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['github'])
def github_message(message):
    git_text = (
        "Вот ссылка на мой GitHub: https://github.com/Fedordenzav "
    )
    bot.send_message(message.chat.id, git_text)

@bot.message_handler(commands=['register'])
def register_user(message):
    if message.chat.id in registered_users:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы! 🎉")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите ваше имя:")
        bot.register_next_step_handler(message, process_name)

def process_name(message):
    name = message.text
    registered_users[message.chat.id] = name
    user_scores[message.chat.id] = 10  
    bot.send_message(message.chat.id, f"{name}, вы успешно зарегистрированы! Теперь вы можете играть. Используйте команду /start для начала.")

@bot.message_handler(commands=['exit'])
def exit_game(message):
    if message.chat.id in registered_users:
        name = registered_users[message.chat.id]
        score = user_scores[message.chat.id]
        
        
        if message.chat.id in current_word:
            del current_word[message.chat.id]  
        if message.chat.id in timer_thread:
            
            timer_thread[message.chat.id].join()  
            del timer_thread[message.chat.id] 

        bot.send_message(message.chat.id, f"{name}, вы вышли из игры. Ваши очки: {score}.")
        help_message(message)  
    else:
        bot.send_message(message.chat.id, "Сначала зарегистрируйтесь с помощью команды /register.")

@bot.message_handler(func=lambda message: True)
def check_word(message):
    if message.chat.id not in registered_users:
        bot.send_message(message.chat.id, "Сначала зарегистрируйтесь с помощью команды /register.")
        return
    global data
    original_word = current_word.get(message.chat.id)
    if original_word and message.text == original_word:
        user_scores[message.chat.id] += 3 
        data.remove(original_word)  
        bot.send_message(message.chat.id, f"Молодец, {registered_users[message.chat.id]}!😁 У вас {user_scores[message.chat.id]} очков.")
        send_new_word(message.chat.id)  
    else:
        bot.send_message(message.chat.id, "Неправильно(😕 Попробуй еще раз!")

try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Произошла ошибка: {e}")