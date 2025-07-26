import logging
import json
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Telegram токен
bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)

# GitHub JSON с базой знаний
VITAMINS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/vitamins.json"
vitamin_knowledge = {}

# Обновление базы
@dp.message_handler(commands=["обновить_базу"])
async def update_base(message: types.Message):
    global vitamin_knowledge
    print("📥 Загружаю базу витаминов...")
    async with aiohttp.ClientSession() as session:
        async with session.get(VITAMINS_URL) as resp:
            if resp.status == 200:
                text = await resp.text()
                vitamin_knowledge = json.loads(text)
                print("✅ База загружена")
                await message.reply("✅ База витаминов загружена!")
            else:
                print("❌ Не удалось загрузить базу")
                await message.reply("⚠️ Ошибка загрузки базы.")

# Ответ на запрос о витамине
@dp.message_handler(lambda msg: msg.text.lower().startswith("витамин"))
async def reply_about_vitamin(message: types.Message):
    query = message.text.lower().strip()
    print(f"🔎 Запрос: {query}")
    for name, info in vitamin_knowledge.items():
        if query in name.lower():
            reply = f"💊 *{name}*\n"
            for key, value in info.items():
                reply += f"• **{key.capitalize()}**: {value}\n"
            await message.reply(reply, parse_mode="Markdown")
            return
    await message.reply("Не нашёл такого витамина 😔")

# Старт
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("🚀 Бот запущен!")
    executor.start_polling(dp, skip_updates=True) 
