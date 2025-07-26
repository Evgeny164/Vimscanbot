
import logging
import os
import json
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ["BOT_TOKEN"])
dp = Dispatcher(bot)

# Ссылки на JSON-базы в репозитории
VITAMINS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/vitamins.json"
MINERALS_URL = "https://raw.githubusercontent.com/Evgeny164/Vimscanbot/main/knowledge/minerals.json"

vitamin_knowledge: dict = {}
mineral_knowledge: dict = {}

@dp.message_handler(commands=["обновить_базу"])
async def update_base(message: types.Message):
    global vitamin_knowledge, mineral_knowledge
    async with aiohttp.ClientSession() as session:
        # Загрузка базы витаминов
        resp1 = await session.get(VITAMINS_URL)
        if resp1.status == 200:
            vitamin_knowledge = await resp1.json()
            logging.info("✔ Vitamins base loaded.")
        else:
            logging.warning(f"✖ Failed to load vitamins.json: {resp1.status}")
        # Загрузка базы минералов
        resp2 = await session.get(MINERALS_URL)
        if resp2.status == 200:
            mineral_knowledge = await resp2.json()
            logging.info("✔ Minerals base loaded.")
        else:
            logging.warning(f"✖ Failed to load minerals.json: {resp2.status}")

    await message.reply("✅ База витаминов и минералов загружена!")

@dp.message_handler()
async def handle_query(message: types.Message):
    text = message.text.lower().strip()
    tokens = text.split()
    found = False

    for token in tokens:
        # Ищем по витаминам
        for name, info in vitamin_knowledge.items():
            if token in name.lower():
                reply = f"💊 *{name}*\n"
                for k, v in info.items():
                    reply += f"• **{k.capitalize()}**: {v}\n"
                await message.reply(reply, parse_mode="Markdown")
                found = True
        # Ищем по минералам
        for name, info in mineral_knowledge.items():
            if token in name.lower():
                reply = f"🧪 *{name}*\n"
                for k, v in info.items():
                    reply += f"• **{k.capitalize()}**: {v}\n"
                await message.reply(reply, parse_mode="Markdown")
                found = True

    if not found:
        await message.reply("😔 Не нашёл таких витаминов или минералов в базе.")

if __name__ == "__main__":
    print("🚀 Bot started!")
    executor.start_polling(dp, skip_updates=True)
