from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread
import asyncio
import random
import os
from config import API_ID, API_HASH, SESSION, PROMO_TEXT

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
flask_app = Flask(__name__)

recent_users = {}

@flask_app.route("/")
def home():
    return "UserBot Running Successfully!"

# Anti Flood Reply
@app.on_message(filters.group & filters.text)
async def auto_reply(client, message: Message):
    if message.from_user.is_self:
        return

    chat_id = message.chat.id
    user_id = message.from_user.id

    last_reply = recent_users.get(user_id, 0)
    current_time = message.date.timestamp()

    # Delay reply if user is sending fast messages
    if current_time - last_reply < 10:
        return

    recent_users[user_id] = current_time
    delay = random.randint(2, 5)
    await asyncio.sleep(delay)
    await message.reply_text(PROMO_TEXT)

def run_flask():
    flask_app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    app.run()
