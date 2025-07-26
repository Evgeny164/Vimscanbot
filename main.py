import logging
import json
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Логирование
logging.basicConfig(level=logging.INFO)

# Telegram
bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)

# Ссылки на GitHub
VITAMINS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/vitamins.json"
MINERALS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/minerals.json"

vitamin_knowledge = {}
mineral_knowledge = {}

@dp.message_handler(commands=["обновить_базу"])
async def update_base(message: types.Message):
    global vitamin_knowledge, mineral_knowledge
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(VITAMINS_URL) as resp1:
                if resp1.status == 200:
                    vitamin_knowledge = json.loads(await resp1.text())
                    logging.info("✅ Vitamins base loaded.")
                else:
                    logging.warning("⚠️ Failed to load vitamins.json")
            async with session.get(MINERALS_URL) as resp2:
                if resp2.status == 200:
                    mineral_knowledge = json.loads(await resp2.text())
                    logging.info("✅ Minerals base loaded.")
                else:
                    logging.warning("⚠️ Failed to load minerals.json")
            await message.reply("✅ База витаминов и минералов загружена!")
        except Exception as e:
            await message.reply(f"❌ Ошибка загрузки базы: {e}")

@dp.message_handler()
async def handle_query(message: types.Message):
    query = message.text.lower().strip()
    # Витамины
    for name, info in vitamin_knowledge.items():
        if query in name.lower():
            reply = f"💊 *{name}*\n"
            for k, v in info.items():
                reply += f"• **{k.capitalize()}**: {v}\n"
            await message.reply(reply, parse_mode="Markdown")
            return
    # Минералы
    for name, info in mineral_knowledge.items():
        if query in name.lower():
            reply = f"🧪 *{name}*\n"
            for k, v in info.items():
                reply += f"• **{k.capitalize()}**: {v}\n"
            await message.reply(reply, parse_mode="Markdown")
            return
    await message.reply("😔 Не нашёл такого витамина или минерала в базе.")

if __name__ == "__main__":
    print("🚀 Бот запущен!")
    executor.start_polling(dp, skip_updates=True)
