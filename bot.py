import sqlite3
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime, timedelta
import requests
import json
import openai
from openai import OpenAI
import schedule
import time
from datetime import datetime, timedelta


def schedule_function():
    
    now = datetime.now()
    if now.minute < 30:
        next_run = now.replace(minute=30, second=0, microsecond=0)
    else:
        next_run = now.replace(hour=now.hour+1, minute=0, second=0, microsecond=0)

    
    schedule.every().day.at(next_run.strftime("%H:%M")).do(Catalizer())
    
  
    half_hour = timedelta(minutes=30)
    while True:
        current_time = datetime.now().strftime("%H:%M")
        next_run = (datetime.strptime(current_time, "%H:%M") + half_hour).strftime("%H:%M")
        schedule.every().day.at(next_run).do(Catalizer())
        print(f"Next function call scheduled at {next_run}")
        time.sleep(30)  




def is_valid_api_key(api_key):
    dateFrom = int((datetime.now() - timedelta(days=90)).timestamp())
    dateTo = int(datetime.now().timestamp())
    url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'
    params = {
        'isAnswered': False,
        'take': 1,
        'skip': 0,
        'order': 'dateDesc',
        'dateFrom': dateFrom,
        'dateTo': dateTo
    }
    headers = {
        'Authorization': api_key
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200: return True
    else: return False


def Check_feedback(api_key):
    dateFrom = int((datetime.now() - timedelta(days=90)).timestamp())
    dateTo = int(datetime.now().timestamp())
    url = 'https://feedbacks-api.wildberries.ru/api/v1/feedbacks'
    params = {
        'isAnswered': False,
        'take': 100,
        'skip': 0,
        'order': 'dateDesc',
        'dateFrom': dateFrom,
        'dateTo': dateTo
    }
    headers = {
        'Authorization': api_key
    }
    response = requests.get(url, headers=headers, params=params)
    res = response.json()
    if response.status_code == 200 and res['data']['countUnanswered'] != 0:
        return res
    else: 
        return False

def get_rating_by_api_key(api_key):
    conn = sqlite3.connect('mydatabase1.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rating FROM users WHERE api_key = ?", (api_key,))
    rating = cursor.fetchone()
    conn.close()
    if rating:
        return rating[0]
    else:
        return None

def tryTosend(res,rating):
    m = {}
    res = res['data']['feedbacks']
    for key in res:
        if key['productValuation'] >= rating: m[res['data']['feedbacks']['text']] = m[res['data']['feedbacks']['id']]
    return m 

def Sender(res, api_key, massive, openai):
    client = OpenAI(api_key=openai)
    ruls = 'Напиши благодарственный ответ на отзыв к покупке на маркетплейсе от имени продавца.Ответ должен соответствовать следующим критериям - ответ не должен содержать заполнители, параметры для вставки (наприер {имя клиента|компания} и т.п.); - клиент имеет женский пол; - не должен содержать информацию от кого этот ответ(например: "Команда продавцов" - такого не должно быть в ответе); - не должно быть предложение клиенту об обмене товара или какой-то компенсации. Пример ответа: Здравствуйте. Спасибо за то, что выбрали нас. Позвольте поблагодарить Вас за отзыв. Мы очень рады, что Вам подошел Наш товар, носите с удовольствием. Будем рады видеть Вас снова. Приятных покупок!  Дальше я передаю сам ответ покупателя:   '
    user_question = ''
    answer = ''
    url = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"
    headers = {
        'Authorization': api_key,  
    }
    for key in massive:
        user_question = key
        try:
            chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": ruls + user_question,
                        }
                    ],
                    model="gpt-3.5-turbo",
                )
            
            answer = chat_completion.choices[0].message.content
            data = {
                'id': massive[key],        
                'text': answer   
            }
            response = requests.patch(url, json=data, headers=headers)
            if response.status_code == 200: return True
        except Exception as e: print(1)


def Catalizer(): 
    api_keys = iterate_api_keys()
    for user_id, api_key in api_keys:
        result = Check_feedback(api_key)
        if result: Sender(result, api_key, tryTosend(result,get_rating_by_api_key(result)))

    

def create_connection():
    connection = sqlite3.connect('mydatabase1.db')
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, 
            api_key TEXT, 
            rating FLOAT DEFAULT 0, 
            attempts INTEGER DEFAULT 0
        )
    """)
    connection.commit()
    return connection

def update_or_create_user_key(user_id, api_key, rating) -> bool:
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT api_key FROM users WHERE id = ?", (user_id,))
    data = cursor.fetchone()
    if data:
        cursor.execute("UPDATE users SET api_key = ?, rating = ? WHERE id = ?", (api_key, rating, user_id))
    else:
        cursor.execute("INSERT INTO users (id, api_key, rating, attempts) VALUES (?, ?, ?, 50)", (user_id, api_key, rating))
    conn.commit()
    conn.close()

def iterate_api_keys():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, api_key, rating, attempts FROM users")
    api_keys = cursor.fetchall()
    conn.close()
    for api_key in api_keys:
        yield api_key

def update_attempts(user_id, attempts):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET attempts = ? WHERE id = ?", (attempts, user_id))
    conn.commit()
    conn.close()

user_states = {}

def get_user_state(user_id):
    return user_states.get(user_id, None)

def set_user_state(user_id, state):
    user_states[user_id] = state




@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 
    btn1 = types.KeyboardButton("Отправить ключ")
    markup.add(btn1)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот, который за тебя будет писать отзывы 💪".format(message.from_user), reply_markup=markup)


temporary_storage = {}

def set_temporary_key(user_id, api_key):
    temporary_storage[user_id] = api_key

def get_temporary_key(user_id):
    return temporary_storage.get(user_id)

@bot.message_handler(content_types=['text'])
def message_func(message):
    user_id = message.chat.id
    if message.text == "Отправить ключ":
        bot.send_message(user_id, "Отправь мне свой API ключ")
        set_user_state(user_id, "awaiting_api_key")
    elif get_user_state(user_id) == "awaiting_api_key":
        api_key = message.text
        set_temporary_key(user_id, api_key)
        set_user_state(user_id, "awaiting_rating")
        bot.send_message(user_id, "Теперь отправь рейтинг ключа от 1 до 5")
    elif get_user_state(user_id) == "awaiting_rating":
        rating = float(message.text)
        if 1 <= rating <= 5:
            api_key = get_temporary_key(user_id)
            if is_valid_api_key(api_key):
                update_or_create_user_key(user_id, api_key, rating)
                bot.send_message(user_id, "Твой API ключ и рейтинг сохранены!")
            else:
                bot.send_message(user_id, "Произошла ошибка, проверь корректность ключа.")
        else:
            bot.send_message(user_id, "Рейтинг должен быть числом от 1 до 5.")
        set_user_state(user_id, None)  




