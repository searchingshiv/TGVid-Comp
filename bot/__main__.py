# Import necessary modules and configurations
from . import *
from .config import *
from .worker import *
from .devtools import *
from .FastTelethon import *
import os
import asyncio
import time
import re
from telethon import events, Button
from datetime import datetime as dt
from pathlib import Path
from aiohttp import web

try:
    bot.start(bot_token=BOT_TOKEN)
except Exception as er:
    LOGS.info(f"Bot failed to start: {er}")

####### HTTP SERVER ########

async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get("/", handle)

####### GENERAL CMDS ########

@bot.on(events.NewMessage(pattern="/start"))
async def start_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await start(e)

@bot.on(events.NewMessage(pattern="/setcode"))
async def setcode_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await coding(e)

@bot.on(events.NewMessage(pattern="/getcode"))
async def getcode_cmd(e):
    print("Sender ID:", e.sender_id)  # Debug log for sender ID
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await getcode(e)

@bot.on(events.NewMessage(pattern="/showthumb"))
async def showthumb_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await getthumb(e)

@bot.on(events.NewMessage(pattern="/logs"))
async def logs_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await getlogs(e)

@bot.on(events.NewMessage(pattern="/cmds"))
async def cmds_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await zylern(e)

@bot.on(events.NewMessage(pattern="/ping"))
async def ping_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await up(e)

@bot.on(events.NewMessage(pattern="/sysinfo"))
async def sysinfo_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await sysinfo(e)

@bot.on(events.NewMessage(pattern="/leech"))
async def leech_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await dl_link(e)

@bot.on(events.NewMessage(pattern="/help"))
async def help_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await ihelp(e)

@bot.on(events.NewMessage(pattern="/renew"))
async def renew_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await renew(e)

@bot.on(events.NewMessage(pattern="/clear"))
async def clear_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await clearqueue(e)

@bot.on(events.NewMessage(pattern="/speed"))
async def speed_cmd(e):
    if str(e.sender_id) not in OWNER and str(e.sender_id) != str(DEV):
        return await e.reply("**Sorry, you're not an authorized user!**")
    await test(e)

########## Direct ###########

@bot.on(events.NewMessage(pattern="/eval"))
async def eval_cmd(e):
    await eval(e)

@bot.on(events.NewMessage(pattern="/bash"))
async def bash_cmd(e):
    await bash(e)

######## Callbacks #########

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"stats(.*)")))
async def stats_callback(e):
    await stats(e)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"skip(.*)")))
async def skip_callback(e):
    await skip(e)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile("help")))
async def help_callback(e):
    await help(e)

########## AUTO ###########

@bot.on(events.NewMessage(incoming=True))
async def auto_process(event):
    if str(event.sender_id) not in OWNER and str(event.sender_id) != str(DEV):
        return await event.reply("**Sorry, you're not an authorized user!**")
    
    if event.photo:
        os.system("rm thumb.jpg")
        await event.client.download_media(event.media, file="/bot/thumb.jpg")
        await event.reply("**Thumbnail saved successfully.**")
    
    await encod(event)

########### Background Task ##########

async def background_task():
    for i in itertools.count():
        try:
            if not WORKING and QUEUE:
                user = int(OWNER.split()[0])
                e = await bot.send_message(user, "**📥 Downloading Queue Files...**")
                s = dt.now()
                try:
                    if isinstance(QUEUE[list(QUEUE.keys())[0]], str):
                        dl = await fast_download(
                            e, list(QUEUE.keys())[0], QUEUE[list(QUEUE.keys())[0]]
                        )
                    else:
                        dl, file = QUEUE[list(QUEUE.keys())[0]]
                        tt = time.time()
                        dl = "downloads/" + dl
                        with open(dl, "wb") as f:
                            ok = await download_file(
                                client=bot,
                                location=file,
                                out=f,
                                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                                    progress(
                                        d,
                                        t,
                                        e,
                                        tt,
                                        f"**📥 Downloading**\n__{dl.replace(f'downloads/', '')}__",
                                    )
                                ),
                            )
                except Exception as r:
                    LOGS.info(f"Download error: {r}")
                    WORKING.clear()
                    QUEUE.pop(list(QUEUE.keys())[0])
                    continue
                # Further processing, compression, and upload logic goes here
        except Exception as err:
            LOGS.info(f"Background task error: {err}")

########### Start Bot and Server ##########

async def start_bot():
    bot.start(bot_token=BOT_TOKEN)
    LOGS.info("Bot has started.")
    await background_task()

if __name__ == "__main__":
    PORT = os.getenv("PORT", "8080")
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    web.run_app(app, port=int(PORT))
