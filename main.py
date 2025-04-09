from pyrogram import Client, filters
from pyrogram.types import Message
from flask import Flask
from threading import Thread
import asyncio
import random
import time
import os
from config import API_ID, API_HASH, SESSION, PROMO_TEXT, DELETE_AFTER, SAFE_DELAY

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
flask_app = Flask(__name__)

recent_users = {}  # Per User Delay
global_last_reply = 0  # Global Delay Control

@flask_app.route("/")
def home():
    return "UserBot Running Smoothly!"

# Auto Leave If No Permission
@app.on_chat_member_updated()
async def check_permissions(_, member):
    if member.new_chat_member.user and member.new_chat_member.user.is_self:
        if not member.new_chat_member.can_send_messages:
            await member.chat.leave()

@app.on_message(filters.group & filters.text)
async def auto_reply(client, message: Message):
    global global_last_reply

    if not message.from_user:  # Skip if from_user is None
        return

    if message.from_user.is_self:  # Don't reply to self message
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    current_time = time.time()

    # Per User Delay Control
    last_reply = recent_users.get((chat_id, user_id), 0)
    if current_time - last_reply < 10:
        return
    recent_users[(chat_id, user_id)] = current_time

    # Global Delay Control
    if current_time - global_last_reply < SAFE_DELAY:
        await asyncio.sleep(SAFE_DELAY)

    global_last_reply = time.time()

    await asyncio.sleep(random.randint(2, 5))  # Random small delay

    try:
        reply = await message.reply_text(PROMO_TEXT)
        await asyncio.sleep(DELETE_AFTER)
        await reply.delete()
    except Exception as e:
        print(f"Error: {e}")

# /rx Command
@app.on_message(filters.command("rx", prefixes=["/", "."]) & filters.group)
async def public_alive(client, message):
    await message.reply("Baby I am Alive 💖")

def run_flask():
    flask_app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    Thread(target=run_flask).start()
    app.run()
