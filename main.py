import logging
import json
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Logging
logging.basicConfig(level=logging.INFO)

# Bot and Dispatcher
bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)

# URL to vitamins.json
VITAMINS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/vitamins.json"
vitamin_knowledge = {}

# Command: /update_base
@dp.message_handler(commands=["обновить_базу"])
async def update_base(message: types.Message):
    global vitamin_knowledge
    logging.info("📥 Updating vitamins base...")
    async with aiohttp.ClientSession() as session:
        async with session.get(VITAMINS_URL) as resp:
            if resp.status == 200:
                text = await resp.text()
                vitamin_knowledge = json.loads(text)
                logging.info("✅ Vitamins base loaded.")
                await message.reply("✅ База витаминов загружена!")
            else:
                logging.warning(f"⚠️ Failed to load base. Code: {resp.status}")
                await message.reply("⚠️ Не удалось загрузить базу знаний.")

# Vitamin query
@dp.message_handler(lambda msg: msg.text.lower().startswith("витамин"))
async def reply_about_vitamin(message: types.Message):
    query = message.text.lower().strip()
    logging.info(f"🔍 User asked: {query}")
    for name, info in vitamin_knowledge.items():
        if query in name.lower():
            response = f"💊 *{name}*\n"
            for key, value in info.items():
                response += f"• **{key.capitalize()}**: {value}\n"
            await message.reply(response, parse_mode="Markdown")
            return
    await message.reply("😔 Не нашёл такого витамина в базе.")

# Start
if __name__ == "__main__":
    print("🚀 Бот запущен!")
    executor.start_polling(dp, skip_updates=True)
