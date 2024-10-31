#    This file is part of the CompressorQueue distribution.
#    Copyright (c) 2021 Danish_00
#    Script Improved by Zylern

import os
import re
import asyncio
from aiohttp import web
from pathlib import Path
from telethon import Button, events
from . import *
from .config import *
from .worker import *
from .devtools import *
from .FastTelethon import *
from datetime import datetime as dt
import time

LOGS.info("Starting...")

try:
    bot.start(bot_token=BOT_TOKEN)
except Exception as er:
    LOGS.info(er)


####### GENERAL CMDS ########

@bot.on(events.NewMessage(pattern=r"/start"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await start(e)


@bot.on(events.NewMessage(pattern=r"/setcode"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await coding(e)


@bot.on(events.NewMessage(pattern=r"/getcode"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await getcode(e)


@bot.on(events.NewMessage(pattern=r"/showthumb"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await getthumb(e)


@bot.on(events.NewMessage(pattern=r"/logs"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await getlogs(e)


@bot.on(events.NewMessage(pattern=r"/cmds"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await zylern(e)


@bot.on(events.NewMessage(pattern=r"/ping"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await up(e)


@bot.on(events.NewMessage(pattern=r"/sysinfo"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await sysinfo(e)


@bot.on(events.NewMessage(pattern=r"/leech"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await dl_link(e)


@bot.on(events.NewMessage(pattern=r"/help"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await ihelp(e)


@bot.on(events.NewMessage(pattern=r"/renew"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await renew(e)


@bot.on(events.NewMessage(pattern=r"/clear"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await clearqueue(e)


@bot.on(events.NewMessage(pattern=r"/speed"))
async def _(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return await e.reply("**Sorry You're not An Authorised User!**")
    await test(e)


########## Direct ###########

@bot.on(events.NewMessage(pattern=r"/eval"))
async def _(e):
    await eval(e)

@bot.on(events.NewMessage(pattern=r"/bash"))
async def _(e):
    await bash(e)


######## Callbacks #########

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"stats(.*)")))
async def _(e):
    await stats(e)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile(b"skip(.*)")))
async def _(e):
    await skip(e)

@bot.on(events.callbackquery.CallbackQuery(data=re.compile("help")))
async def _(e):
    await help(e)


########## AUTO ###########

@bot.on(events.NewMessage(incoming=True))
async def _(event):
    if str(event.sender_id) not in OWNER and event.sender_id != DEV:
        return await event.reply("**Sorry You're not An Authorised User!**")
    if not event.photo:
        return
    os.system("rm thumb.jpg")
    await event.client.download_media(event.media, file="/bot/thumb.jpg")
    await event.reply("**Thumbnail Saved Successfully.**")


@bot.on(events.NewMessage(incoming=True))
async def _(e):
    await encod(e)


async def something():
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
                    LOGS.info(r)
                    WORKING.clear()
                    QUEUE.pop(list(QUEUE.keys())[0])
                es = dt.now()
                kk = dl.split("/")[-1]
                aa = kk.split(".")[-1]
                newFile = dl.replace(f"downloads/", "").replace(f"_", " ")
                rr = "encode"
                bb = kk.replace(f".{aa}", ".mkv")
                out = f"{rr}/{bb}"
                thum = "thumb.jpg"
                dtime = ts(int((es - s).seconds) * 1000)
                hehe = f"{out};{dl};{list(QUEUE.keys())[0]}"
                wah = code(hehe)
                nn = await e.edit(
                    "**🗜 Compressing...**",
                    buttons=[
                        [Button.inline("STATS", data=f"stats{wah}")],
                        [Button.inline("CANCEL", data=f"skip{wah}")],
                    ],
                )
                cmd = f"""ffmpeg -i "{dl}" {ffmpegcode[0]} "{out}" -y"""
                process = await asyncio.create_subprocess_shell(
                    cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await process.communicate()
                er = stderr.decode()
                try:
                    if er:
                        await e.edit(str(er) + "\n\n**ERROR**")
                        QUEUE.pop(list(QUEUE.keys())[0])
                        os.remove(dl)
                        os.remove(out)
                        continue
                except BaseException:
                    pass
                ees = dt.now()
                ttt = time.time()
                await nn.delete()
                nnn = await e.client.send_message(e.chat_id, "**📤 Uploading...**")
                with open(out, "rb") as f:
                    ok = await upload_file(
                        client=e.client,
                        file=f,
                        name=out,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, nnn, ttt, f"**📤 Uploading**\n__{out.replace(f'encode/', '')}__")
                        ),
                    )
                await nnn.delete()
                org = int(Path(dl).stat().st_size)
                com = int(Path(out).stat().st_size)
                pe = 100 - ((com / org) * 100)
                per = str(f"{pe:.2f}") + "%"
                eees = dt.now()
                x = dtime
                xx = ts(int((ees - es).seconds) * 1000)
                xxx = ts(int((eees - ees).seconds) * 1000)
                a1 = await info(dl, e)
                a2 = await info(out, e)
                dk = f"<b>File Name:</b> {newFile}\n\n<b>Original File Size:</b> {hbs(org)}\n<b>Encoded File Size:</b> {hbs(com)}\n<b>Encoded Percentage:</b> {per}\n\n<b>Get Mediainfo Here:</b> <a href='{a1}'>Before</a>/<a href='{a2}'>After</a>\n\n<i>Downloaded in {x}\nEncoded in {xx}\nUploaded in {xxx}</i>"
                ds = await e.client.send_file(
                    e.chat_id, file=ok, force_document=True, caption=dk, link_preview=False, thumb=thum, parse_mode="html"
                )
                QUEUE.pop(list(QUEUE.keys())[0])
                os.remove(dl)
                os.remove(out)
            else:
                await asyncio.sleep(3)
        except Exception as err:
            LOGS.info(err)


# Web server to avoid Render's port error
async def handle(request):
    return web.Response(text="Bot is running.")

app = web.Application()
app.router.add_get("/", handle)
port = int(os.environ.get("PORT", 5000))
web_runner = web.AppRunner(app)

async def start_web_server():
    await web_runner.setup()
    site = web.TCPSite(web_runner, '0.0.0.0', port)
    await site.start()

# Start the bot and web server together
LOGS.info("Bot has started.")
with bot:
    bot.loop.run_until_complete(start_web_server())
    bot.loop.run_until_complete(something())
    bot.loop.run_forever()
