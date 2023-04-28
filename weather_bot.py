import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import telegram_par
import weather_api
import emoji

lang = 'en' #'ru'
TOKEN = telegram_par.token
API_KEY = weather_api.api_key
#cat_url = 'https://cataas.com/cat'
#cat_gif_url = 'https://cataas.com/cat/gif'
URL_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'
URL_WEEKLY_WEATHER_API = 'api.openweathermap.org/data/2.5/forecast/daily'
GEOCODER_URL = 'http://api.openweathermap.org/geo/1.0/direct'
GEOCODER_PARAMS = {
    'appid': API_KEY
}

EMOJI_CODE = emoji.emojis

bot = telebot.TeleBot(TOKEN)
#keyboard.add(KeyboardButton('Котика'))
#keyboard.add(KeyboardButton('Видео-котика'))
if lang == 'en':
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Get weather (needs geolocation)', request_location=True))
    keyboard.add(KeyboardButton('Change language'))
    keyboard.add(KeyboardButton('About program'))
elif lang == 'ru':
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Получить погоду (требуется геопозиция)', request_location=True))
    keyboard.add(KeyboardButton('Сменить язык'))
    keyboard.add(KeyboardButton('О программе'))
'''
def get_cat():
    response = requests.get(cat_url)
    return response.content
def get_gif_cat():
    response = requests.get(cat_gif_url)
    return response.content
'''
def get_city_coords(city):
    GEOCODER_PARAMS['q'] = city
    json = requests.get(GEOCODER_URL, GEOCODER_PARAMS).json()
    lat, lon = json[0]['lat'], json[0]['lon']
    return lat, lon

def get_weather(lat, lon):
    params = {'lat': lat,
              'lon': lon,
              'lang': 'ru',
              'units': 'metric',
              'appid': API_KEY}
    response = requests.get(url=URL_WEATHER_API, params=params).json()
    city_name = response['name']
    description = response['weather'][0]['description']
    code = response['weather'][0]['id']
    temp = response['main']['temp']
    temp_feels_like = response['main']['feels_like']
    humidity = response['main']['humidity']
    emoji = EMOJI_CODE[code]
    message = f'🏙 Погода в: {city_name}\n'
    message += f'{emoji} {description.capitalize()}.\n'
    message += f'🌡 Температура {temp}°C.\n'
    message += f'🌡 Ощущается как {temp_feels_like}°C.\n'
    message += f'💧 Влажность воздуха {humidity}%.\n'
    return message

def get_weather_en(lat, lon):
    params = {'lat': lat,
              'lon': lon,
              'lang': 'en',
              'units': 'metric',
              'appid': API_KEY}
    response = requests.get(url=URL_WEATHER_API, params=params).json()
    city_name = response['name']
    description = response['weather'][0]['description']
    code = response['weather'][0]['id']
    temp = response['main']['temp']
    temp_feels_like = response['main']['feels_like']
    humidity = response['main']['humidity']
    emoji = EMOJI_CODE[code]
    message = f'🏙 Weather in: {city_name}\n'
    message += f'{emoji} {description.capitalize()}.\n'
    message += f'🌡 Temperature: {temp}°C.\n'
    message += f'🌡 Feels like: {temp_feels_like}°C.\n'
    message += f'💧 Humidity: {humidity}%.\n'
    return message

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    if lang == 'en':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Get weather (needs geolocation)', request_location=True))
        keyboard.add(KeyboardButton('Change language'))
        keyboard.add(KeyboardButton('About program'))
    elif lang == 'ru':
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Получить погоду (требуется геопозиция)', request_location=True))
        keyboard.add(KeyboardButton('Сменить язык'))
        keyboard.add(KeyboardButton('О программе'))
    if lang == 'ru': text = 'Отправь мне свою геолокацию и я отправлю тебе погоду в твоём городе.'
    elif lang == 'en': text = 'Send your geolocation to get the weather in your city'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def send_weather(message):
    lon = message.location.longitude
    lat = message.location.latitude
    result = get_weather(lat, lon)
    bot.send_message(message.chat.id, result, reply_markup=keyboard)
    result = get_weather_en(lat, lon)
    bot.send_message(message.chat.id, result, reply_markup=keyboard)
'''
@bot.message_handler(regexp=r'видео-кот\.*')
def cat_video(message):
    bot.send_video(message.chat.id, get_gif_cat()) 
    
@bot.message_handler(regexp=r'кот\.*')
def cat_image(message):
    bot.send_photo(message.chat.id, get_cat())
'''
@bot.message_handler(regexp='О программе')
def send_about(message):
    text = 'Бот позволяет получить погоду в текущем местоположении.\n'
    text += 'Чтобы получить погоду в твоём городе отправь свою геолокацию\n'
    text += 'Сайт с погодой: https://openweathermap.org.\n'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(regexp='About program')
def send_about_en(message):
    text = 'Bot can send you weather in your geolocation.\n'
    text += 'To get weather in your city, you need to send to bot your geolocation\n'
    text += 'Weather website: https://openweathermap.org.\n'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)
    
@bot.message_handler(commands=['weather'])
def help_weather(message):
    if lang == 'ru':
        text = 'Отправьте боту название вашего города/вашу геолокацию/координаты вашего города, и он отправит погоду в вашем городе в данный момент'
    elif lang == 'en':
        text = 'Send to bot your city name/your geolocation/coordinates of your city, and it sends you a weather in your city at the moment'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(regexp='погода\.*')
def weather_message(message):
    try:
        coords = list(map(float, message.text.split()[1:]))
        result = get_weather(coords[0], coords[1])
        bot.send_message(message.chat.id, result, reply_markup=keyboard)
    except ValueError:
        city = message.text.split()[1:]
        for i in city:
            result = get_weather(*get_city_coords(i))
            bot.send_message(message.chat.id, result, reply_markup=keyboard)

@bot.message_handler(regexp='weather\.*')
def weather_message_en(message):
    try:
        coords = list(map(float, message.text.split()[1:]))
        result = get_weather_en(coords[0], coords[1])
        bot.send_message(message.chat.id, result, reply_markup=keyboard)
    except ValueError:
        city = message.text.split()[1:]
        for i in city:
            result = get_weather_en(*get_city_coords(i))
            bot.send_message(message.chat.id, result, reply_markup=keyboard)

@bot.message_handler(regexp='сменить язык\.*')
def change_lang(message):
    global lang
    lang = 'en'
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Get weather (needs geolocation)', request_location=True))
    keyboard.add(KeyboardButton('Change language'))
    keyboard.add(KeyboardButton('About program'))
    bot.send_message(message.chat.id, 'Now language is english', reply_markup=keyboard)
    print (lang)

@bot.message_handler(regexp='change lang\.*')
def change_lang_en(message):
    global lang
    lang = 'ru'
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Получить погоду (требуется геопозиция)', request_location=True))
    keyboard.add(KeyboardButton('Сменить язык'))
    keyboard.add(KeyboardButton('О программе'))
    bot.send_message(message.chat.id, 'Теперь язык - русский', reply_markup=keyboard)
    print (lang)

bot.infinity_polling()
