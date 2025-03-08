import os
import asyncio
import yt_dlp
import http.client
import json
import urllib.parse
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile

# 🔑 RapidAPI API kaliti
RAPIDAPI_KEY = "1e45640c90msh48a86a3d2613653p14d913jsn7bb4fb9b59a5"

# 🤖 Telegram bot tokeni
BOT_TOKEN = "7577882781:AAFP4ezuSzNg3pH5Aij1LZ18LB2687b_mPc"

# 🔥 Telegram botni sozlash
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🚀 Start komandasi
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("📥 Instagram video yuklab beruvchi botga xush kelibsiz!\n🔗 Video havolasini yuboring.")

# 📩 Instagram videolarini yuklab olish
@dp.message()
async def handle_video(message: Message):
    url = message.text.strip()

    if "instagram.com" in url:
        await message.answer("⏳ Video yuklanmoqda, biroz kuting...")

        # 📌 1️⃣ Avval API orqali yuklab olishga harakat qilamiz
        video_url = await download_instagram_video_api(url)

        if video_url:
            video_path = await download_video(video_url)
        else:
            # 📌 2️⃣ API ishlamasa, yt-dlp orqali yuklab olishga harakat qilamiz
            
            video_path = await download_instagram_video_yt_dlp(url)

        if video_path:
            await message.answer_video(FSInputFile(video_path), caption="✅ Mana sizning videongiz!")

            # 🔥 Yuklangan videoni o‘chirib tashlaymiz
            os.remove(video_path)
        else:
            await message.answer("❌ Video yuklab bo‘lmadi! URL-ni tekshiring yoki boshqa video jo‘nating.")
    else:
        await message.answer("❌ Iltimos, Instagram video havolasini yuboring!")

# 📌 1️⃣ RapidAPI orqali Instagram videolarini yuklab olish
async def download_instagram_video_api(url):
    encoded_url = urllib.parse.quote(url, safe="")
    conn = http.client.HTTPSConnection("instagram-downloader-download-instagram-videos-stories1.p.rapidapi.com")

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "instagram-downloader-download-instagram-videos-stories1.p.rapidapi.com"
    }

    conn.request("GET", f"/get-info-rapidapi?url={encoded_url}", headers=headers)
    response = conn.getresponse()
    data = response.read().decode("utf-8")

    try:
        json_data = json.loads(data)
        return json_data.get("video", None)  # Agar video URL bo‘lsa, uni qaytaradi
    except json.JSONDecodeError:
        return None

# 📌 2️⃣ `yt-dlp` orqali Instagram videolarini yuklab olish
async def download_instagram_video_yt_dlp(url):
    video_path = "video.mp4"
    ydl_opts = {
        'outtmpl': video_path,
        'format': 'best[ext=mp4]',
        'quiet': True,
    }

    try:
        loop = asyncio.get_event_loop()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await loop.run_in_executor(None, ydl.download, [url])
        return video_path
    except Exception as e:
        print(f"❌ `yt-dlp` bilan yuklab olishda xatolik: {e}")
        return None

# 📌 3️⃣ Yuklangan videoni saqlash (API yoki `yt-dlp` dan kelgan videoni yuklab olish)
async def download_video(video_url):
    video_path = "video.mp4"

    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as resp:
            if resp.status == 200:
                with open(video_path, "wb") as f:
                    f.write(await resp.read())
                return video_path
    return None

# 🔥 Botni ishga tushirish
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
