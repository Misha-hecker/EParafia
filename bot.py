import asyncio
import json
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

# 1. Завантажуємо токен з твого файлу
load_dotenv("token.env")
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    exit("Помилка: Токен не знайдено у файлі token.env!")

bot = Bot(token=TOKEN)
dp = Dispatcher()
DATA_FILE = "users.json"

# --- Логіка збереження даних ---

def load_data():
    """Читаємо бали з файлу"""
    if not os.path.exists(DATA_FILE) or os.stat(DATA_FILE).st_size == 0:
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_data(data):
    """Записуємо бали у файл"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- Обробка команд ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! Я бот для нарахування балів.\n"
        "Напиши число (наприклад, 10 або -5), щоб змінити свій рахунок.\n"
        "Команда /my_score — показати твій баланс."
    )

@dp.message(Command("my_score"))
async def cmd_score(message: types.Message):
    data = load_data()
    user_id = str(message.from_user.id)
    score = data.get(user_id, 0)
    await message.answer(f"Твій поточний рахунок: {score} балів.")

@dp.message(F.text.regexp(r'^-?\d+$'))
async def add_points(message: types.Message):
    """Додаємо бали, якщо користувач надіслав число"""
    points = int(message.text)
    user_id = str(message.from_user.id)
    
    data = load_data()
    # Оновлюємо значення (якщо користувача немає, беремо 0)
    data[user_id] = data.get(user_id, 0) + points
    save_data(data)
    
    await message.answer(f"Нараховано: {points}. Тепер у тебе: {data[user_id]} балів.")

async def main():
    print("Бот запущений...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений.")