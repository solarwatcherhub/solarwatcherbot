import os
import time
import requests
from bs4 import BeautifulSoup
import telebot

# ====== НАСТРОЙКИ ======
BOT_TOKEN = "8120317095:AAEL10PI27VL40oPZ5b9tQBuCh7dTXJDbYQ"  # твой Telegram токен
CHANNEL_NAME = "@solarwatcherhub"                              # твой канал (собака обязательна)
NEWS_URL = "https://www.solarham.net/"                         # сайт для новостей
LAST_POST_FILE = "last_post.txt"                               # файл для отслеживания, что уже отправлено

bot = telebot.TeleBot(BOT_TOKEN)

# ====== ЗАГРУЗКА ID ПОСЛЕДНЕЙ НОВОСТИ ======
def get_last_post():
    if os.path.exists(LAST_POST_FILE):
        with open(LAST_POST_FILE, "r") as file:
            return file.read().strip()
    return ""

def save_last_post(post_id):
    with open(LAST_POST_FILE, "w") as file:
        file.write(post_id)

# ====== ПАРСИНГ НОВОСТЕЙ С SOLARHAM ======
def get_latest_news():
    response = requests.get(NEWS_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Форматируем дату под стиль сайта, например: May 07, 2025
    today_str = time.strftime("%B %d, %Y")

    font_tags = soup.find_all("font")
    for tag in font_tags:
        if today_str in tag.text:
            title = f"Space Weather for {today_str}"
            summary = tag.text.strip()
            link = NEWS_URL
            return title, summary, link

    return None, None, None

# ====== ОТПРАВКА В TELEGRAM ======
def send_news(title, summary, link):
    message = f"<b>{title}</b>\n\n{summary}\n\n<a href='{link}'>Читать подробнее</a>"
    bot.send_message(CHANNEL_NAME, message, parse_mode="HTML")

# ====== ОСНОВНОЙ ЦИКЛ ======
def main():
    while True:
        try:
            last_post = get_last_post()
            title, summary, link = get_latest_news()
            if title and title != last_post:
                send_news(title, summary, link)
                save_last_post(title)
        except Exception as e:
            print(f"Ошибка: {e}")
        
        time.sleep(600)  # проверка каждые 10 минут

if __name__ == "__main__":
    main()
