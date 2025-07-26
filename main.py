import logging
import json
import aiohttp
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)

# Ссылки на базы
VITAMINS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/vitamins.json"
MINERALS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/minerals.json"

vitamin_knowledge = {}
mineral_knowledge = {}

@dp.message_handler(commands=["обновить_базу"])
async def update_base(message: types.Message):
    global vitamin_knowledge, mineral_knowledge
    async with aiohttp.ClientSession() as session:
        try:
            # Витамины
            async with session.get(VITAMINS_URL) as resp1:
                if resp1.status == 200:
                    vitamin_knowledge = json.loads(await resp1.text())
                    logging.info("✅ Vitamins base loaded.")
                else:
                    logging.warning("❌ Failed to load vitamins.json")

            # Минералы
            async with session.get(MINERALS_URL) as resp2:
                if resp2.status == 200:
                    mineral_knowledge = json.loads(await resp2.text())
                    logging.info("✅ Minerals base loaded.")
                else:
                    logging.warning("❌ Failed to load minerals.json")

            await message.reply("✅ База витаминов и минералов загружена!")

        except Exception as e:
            logging.error(f"❌ Ошибка при загрузке базы: {e}")
            await message.reply(f"❌ Ошибка загрузки базы: {e}")

@dp.message_handler()
async def handle_query(message: types.Message):
    query = message.text.lower().strip()
    logging.info(f"🔍 User asked: {query}")

    for name, info in vitamin_knowledge.items():
        if query in name.lower():
            reply = f"💊 *{name}*\n"
            for k, v in info.items():
                reply += f"•
