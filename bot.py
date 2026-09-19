import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

TOKEN = os.getenv("BOT_TOKEN", "8705937681:AAGwYjI4QqzA5GqdB77YULEGqifbQLRkdKg")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет! Отправь мне ссылку на видео из TikTok, и я скачаю его без водяного знака.")

@dp.message()
async def echo_handler(message: types.Message):
    if "tiktok.com" in message.text:
        await message.answer("Обрабатываю ссылку на TikTok...")
    else:
        await message.answer("Пожалуйста, отправьте корректную ссылку на TikTok!")

async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def main():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
