import os
import time
import requests
from bs4 import BeautifulSoup
import telebot

# Укажи свои данные здесь
BOT_TOKEN = "8120317095:AAEL10PI27VL40oPZ5b9tQBuCh7dTXJDbYQ"
CHANNEL_NAME = "@solarwatcherhub"
NEWS_URL = "https://www.solarham.net/"

bot = telebot.TeleBot(BOT_TOKEN)

# Файл для хранения ID последнего поста
LAST_POST_FILE = "last_post.txt"

def get_last_post():
    if os.path.exists(LAST_POST_FILE):
        with open(LAST_POST_FILE, "r") as file:
            return file.read().strip()
    return ""

def save_last_post(post_id):
    with open(LAST_POST_FILE, "w") as file:
        file.write(post_id)

def get_latest_news():
    response = requests.get(NEWS_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем блок с последней новостью
    breaking_blocks = soup.find_all(string=lambda text: "BREAKING" in text)
    if not breaking_blocks:
        return None, None, None

    block = breaking_blocks[0].find_parent("table")
    if not block:
        return None, None, None

    # Пример парсинга - адаптируй при необходимости
    text = block.get_text(separator="\n", strip=True)
    title = text.split("\n")[0]
    summary = "\n".join(text.split("\n")[1:])

    return title, summary, NEWS_URL

def send_news(title, summary, link):
    message = f"<b>{title}</b>\n\n{summary}\n\n<a href='{link}'>Читать подробнее</a>"
    bot.send_message(CHANNEL_NAME, message, parse_mode="HTML")

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

        time.sleep(600)  # Проверка каждые 10 минут

if __name__ == "__main__":
    main()
