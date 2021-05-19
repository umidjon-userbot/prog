# flake8: noqa F405
"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import time
from os import path

from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pyrogram import Client
from pyromod import listen
from Python_ARQ import ARQ
from telegraph import Telegraph

print("[INFO]: INITIALIZING")
is_config = path.exists("config.py")
if is_config:
    from config import *
else:
    from sample_config import *

listen = listen
USERBOT_PREFIX = USERBOT_PREFIX
GBAN_LOG_GROUP_ID = GBAN_LOG_GROUP_ID
SUDOERS = SUDO_USERS_ID
FERNET_ENCRYPTION_KEY = FERNET_ENCRYPTION_KEY
WELCOME_DELAY_KICK_SEC = WELCOME_DELAY_KICK_SEC
LOG_GROUP_ID = LOG_GROUP_ID
MESSAGE_DUMP_CHAT = MESSAGE_DUMP_CHAT
MOD_LOAD = []
MOD_NOLOAD = []
bot_start_time = time.time()

# MongoDB client
print("[INFO]: LOADING MONGODB")
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.wbb


async def load_sudoers():
    global SUDOERS
    print("[INFO]: LOADING SUDOERS")
    sudoersdb = db.sudoers
    sudoers = await sudoersdb.find_one({"sudo": "sudo"})
    sudoers = [] if not sudoers else sudoers["sudoers"]
    for user_id in SUDOERS:
        if user_id not in sudoers:
            sudoers.append(user_id)
            await sudoersdb.update_one(
                {"sudo": "sudo"}, {"$set": {"sudoers": sudoers}}, upsert=True
            )
    SUDOERS = (SUDOERS + sudoers) if sudoers else SUDOERS


loop = asyncio.get_event_loop()
loop.run_until_complete(load_sudoers())

if not HEROKU:
    print("[INFO]: LOADING USERBOT CLIENT")
    app2 = Client(
        "userbot", phone_number=PHONE_NUMBER, api_id=API_ID, api_hash=API_HASH
    )
else:
    print("[INFO]: LOADING USERBOT CLIENT")
    app2 = Client(SESSION_STRING, api_id=API_ID, api_hash=API_HASH)

# Bot client
print("[INFO]: LOADING BOT CLIENT")
app = Client("wbb", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH)
# ARQ client
print("[INFO]: LOADING ARQ")
arq = ARQ(ARQ_API_URL, ARQ_API_KEY)
# Telegraph client
print("[INFO]: LOADING TELEGRAPH")
telegraph = Telegraph()
telegraph.create_account(short_name="wbb")

BOT_ID = 0
BOT_NAME = ""
BOT_USERNAME = ""
BOT_MENTION = ""
BOT_DC_ID = 0
USERBOT_ID = 0
USERBOT_NAME = ""
USERBOT_USERNAME = ""
USERBOT_DC_ID = 0
USERBOT_MENTION = ""


def get_info(app, app2):
    global BOT_ID, BOT_NAME, BOT_USERNAME, BOT_DC_ID, BOT_MENTION
    global USERBOT_ID, USERBOT_NAME, USERBOT_USERNAME, USERBOT_DC_ID, USERBOT_MENTION
    getme = app.get_me()
    getme2 = app2.get_me()
    BOT_ID = getme.id
    USERBOT_ID = getme2.id
    if getme.last_name:
        BOT_NAME = getme.first_name + " " + getme.last_name
    else:
        BOT_NAME = getme.first_name
    BOT_USERNAME = getme.username
    BOT_MENTION = getme.mention
    BOT_DC_ID = getme.dc_id

    if getme2.last_name:
        USERBOT_NAME = getme2.first_name + " " + getme2.last_name
    else:
        USERBOT_NAME = getme2.first_name
    USERBOT_USERNAME = getme2.username
    USERBOT_MENTION = getme2.mention
    USERBOT_DC_ID = getme2.dc_id


print("[INFO]: STARTING BOT CLIENT")
app.start()
print("[INFO]: STARTING USERBOT CLIENT")
app2.start()
get_info(app, app2)

if USERBOT_ID not in SUDOERS:
    SUDOERS.append(USERBOT_ID)
