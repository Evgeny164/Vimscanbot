import logging
import json
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Telegram
bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)

# Ссылки
VITAMINS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/vitamins.json"
MINERALS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/minerals.json"

vitamin_knowledge = {}
mineral_knowledge = {}

# Обновление базы
@dp.message_handler(commands=["обновить_базу"])
async def update_base(message: types.Message):
    global vitamin_knowledge, mineral_knowledge
    async with aiohttp.ClientSession() as session:
        # Витамины
        async with session.get(VITAMINS_URL) as resp1:
            if resp1.status == 200:
                text1 = await resp1.text()
                vitamin_knowledge = json.loads(text1)
                logging.info("✅ Vitamins base loaded.")
            else:
                logging.warning("❌ Failed to load vitamins.")

        # Минералы
        async with session.get(MINERALS_URL) as resp2:
            if resp2.status == 200:
                text2 = await resp2.text()
                mineral_knowledge = json.loads(text2)
                logging.info("✅ Minerals base loaded.")
            else:
                logging.warning("❌ Failed to load minerals.")

    await message.reply("✅ База витаминов и минералов загружена!")

# Ответы
@dp.message_handler()
async def handle_query(message: types.Message):
    query = message.text.lower().strip()
    logging.info(f"🔍 User asked: {query}")

    for name, info in vitamin_knowledge.items():
        if query in name.lower():
            reply = f"💊 *{name}*\n"
            for k, v in info.items():
                reply += f"• **{k.capitalize()}**: {v}\n"
            await message.reply(reply, parse_mode="Markdown")
            return

    for name, info in mineral_knowledge.items():
        if query in name.lower():
            reply = f"🧪 *{name}*\n"
            for k, v in info.items():
                reply += f"• **{k.capitalize()}**: {v}\n"
            await message.reply(reply, parse_mode="Markdown")
            return

    await message.reply("😔 Не нашёл такого витамина или минерала в базе.")

# Запуск
if __name__ == "__main__":
    print("🚀 Бот запущен!")
    executor.start_polling(dp, skip_updates=True)
