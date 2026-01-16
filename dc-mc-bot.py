from dotenv import load_dotenv
import discord
import requests
import asyncio
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1044367569475338240
MC_SERVER = "shrimpsy.aternos.me:36312"
CHECK_INTERVAL = 900

print("TOKEN = ", TOKEN)

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_status = None


async def check_server_status():
    global last_status
    await client.wait_until_ready()

    # ПРИНУДИТЕЛЬНО получаем канал
    channel = await client.fetch_channel(CHANNEL_ID)
    print("Канал найден:", channel)

    while True:
        try:
            url = f"https://api.mcsrvstat.us/2/{MC_SERVER}"
            r = requests.get(url, timeout=10)
            data = r.json()

            online = data.get("online", False)

            print("RAW DATA:", data)
            print("ONLINE =", online)

            # диагностическое сообщение КАЖДЫЙ РАЗ
            await channel.send(
                f"🧪 Діагностика:\n"
                f"Сервер: {MC_SERVER}\n"
                f"Статус: {'ONLINE' if online else 'OFFLINE'}"
            )

            last_status = online

        except Exception as e:
            print("Помилка:", e)
            await channel.send(f"❌ Помилка: {e}")

        await asyncio.sleep(CHECK_INTERVAL)


@client.event
async def on_ready():
    print(f"Бот запущений як {client.user}")

    # тестовое сообщение
    channel = await client.fetch_channel(CHANNEL_ID)
    await channel.send("🧪 Бот запущений і може писати в канал")

    asyncio.create_task(check_server_status())


client.run(TOKEN)