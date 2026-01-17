from telethon import TelegramClient, events
from datetime import datetime
import json
import os

# ================= CONFIG =================
API_ID = 33000715           # আপনার Telegram API_ID
API_HASH = "77b519164b6a7c2a491b484149caf3d1"  # আপনার Telegram API_HASH
SESSION_NAME = "@saidulbhai34"  # Name for the session file

# ===== UNIC STYLE ENGLISH AUTO-REPLY =====
AUTO_REPLY_TEXT = """
╔═━┈┈🩸 𝗖𝗢𝗠𝗠𝗔𝗡𝗗 𝗠𝗘𝗡𝗨 🩸┈┈━═╗
║
║ 💀 𝐇𝐞𝐥𝐥𝐨! 𝐈 𝐚𝐦 𝐜𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 𝐨𝐟𝐟𝐥𝐢𝐧𝐞.
║ ⏳ 𝐈 𝐡𝐚𝐯𝐞 𝐫𝐞𝐜𝐞𝐢𝐯𝐞𝐝 𝐲𝐨𝐮𝐫 𝐦𝐞𝐬𝐬𝐚𝐠𝐞, 𝐰𝐢𝐥𝐥 𝐫𝐞𝐩𝐥𝐲 𝐬𝐡𝐨𝐫𝐭𝐥𝐲.
║ 🌑 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐩𝐚𝐭𝐢𝐞𝐧𝐭𝐥𝐲 𝐮𝐧𝐭𝐢𝐥 𝐈 𝐜𝐨𝐦𝐞 𝐨𝐧𝐥𝐢𝐧𝐞.
║
║ ⚜️ 𝐒𝐄𝐑𝐕𝐈𝐂𝐄𝐒
║ ┏🤖 𝐓𝐂𝐏 𝐁𝐨𝐭 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭
║ ┣🌟 𝐔𝐈𝐃 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 & 𝐀𝐮𝐭𝐨-𝐋𝐢𝐤𝐞 𝐒𝐲𝐬𝐭𝐞𝐦𝐬
║ ┗🔥 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐕𝐈𝐏 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐜𝐞
║
║ 👑 𝐒𝐚𝐢𝐝𝐮𝐥 𝐎𝐟𝐟𝐢𝐜𝐢𝐚𝐥
║ 🩸 𝐏𝐚𝐢𝐝 / 𝐓𝐫𝐮𝐬𝐭𝐞𝐝 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐎𝐧𝐥𝐲
╚═━┈┈🩸 𝐄𝐍𝐃 𝐎𝐅 𝐌𝐄𝐒𝐒𝐀𝐆𝐄 🩸┈┈━═╝
"""

# File to track last reply per user
DATA_FILE = "last_reply.json"

# Load previous data or initialize
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        LAST_REPLY = json.load(f)
else:
    LAST_REPLY = {}

# Initialize Telegram client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Reset daily replies
def reset_daily():
    today = datetime.now().strftime("%Y-%m-%d")
    if LAST_REPLY.get("date") != today:
        LAST_REPLY.clear()
        LAST_REPLY["date"] = today
        with open(DATA_FILE, "w") as f:
            json.dump(LAST_REPLY, f)

# Check if user already received reply today
def has_replied_today(user_id):
    reset_daily()
    return str(user_id) in LAST_REPLY

# Update last reply date
def update_last_reply(user_id):
    LAST_REPLY[str(user_id)] = True
    with open(DATA_FILE, "w") as f:
        json.dump(LAST_REPLY, f)

# Auto-reply handler
@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    # Only private chats
    if not event.is_private:
        return

    # Get full sender info
    sender = await event.get_sender()
    if sender is None:
        return

    # Ignore bots & yourself
    me = await client.get_me()
    if sender.bot or sender.id == me.id:
        return

    user_id = sender.id

    # Only reply once per day
    if has_replied_today(user_id):
        return

    # Send UNIC style auto-reply
    await event.reply(AUTO_REPLY_TEXT)
    update_last_reply(user_id)

print("✅ UNIC Private Inbox Auto-Reply (1 per day) Running...")
client.start()
client.run_until_disconnected()