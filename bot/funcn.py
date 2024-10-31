# This file is part of the CompressorQueue distribution.
# Copyright (c) 2021 Danish_00
# Script Improved by Zylern

from . import *
from .config import *
from .worker import *
from urllib.parse import unquote
from asyncio import create_subprocess_shell as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
import psutil, os, signal, sys, platform, sysconfig, math, time
from bot import ffmpegcode, LOG_FILE_NAME
from psutil import disk_usage, cpu_percent, virtual_memory, Process as psprocess
from datetime import datetime as dt
import aiohttp, asyncio

WORKING = []
QUEUE = {}
OK = {}
uptime = dt.now()
os.system(f"wget {THUMBNAIL} -O thumb.jpg")

# Ensure required directories exist
for dir_name in ["downloads", "encode", "thumb"]:
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

def code(data):
    OK.update({len(OK): data})
    return str(len(OK) - 1)


def decode(key):
    if OK.get(int(key)):
        return OK[int(key)]
    return

# Convert seconds to HH:MM:SS format
def stdr(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Convert milliseconds to time format
def ts(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d, {hours}h, {minutes}m, {seconds}s, {milliseconds}ms" if days else f"{hours}h, {minutes}m, {seconds}s"

# Convert bytes to human-readable format
def hbs(size):
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return f"{round(size, 2)} {dict_power_n[raised_to_pow]}B"

# Progress tracking function with estimated time and size
async def progress(current, total, e, start, type_of_ps, file=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff if diff > 0 else 0
        time_to_completion = round((total - current) / speed) * 1000 if speed > 0 else 0
        progress_str = "{0}{1} **{2}%**\n\n".format(
            "".join(["■" for _ in range(math.floor(percentage / 10))]),
            "".join(["□" for _ in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2),
        )
        tmp = (
            progress_str
            + f"**✅ Progress:** {hbs(current)} of {hbs(total)}\n"
            + f"**📁 Total Size:** {hbs(total)}\n"
            + f"**🚀 Speed:** {hbs(speed)}/s\n"
            + f"**⏰ Estimated Time Left:** {ts(time_to_completion)}\n"
        )
        if file:
            await e.edit(f"{type_of_ps}\n\n**File Name:** {file}\n\n{tmp}")
        else:
            await e.edit(f"{type_of_ps}\n\n{tmp}")

# Command to check system speed
async def test(e):
    try:
        zylern = "speedtest --simple"
        fetch = await asyncrunapp(zylern, stdout=asyncPIPE, stderr=asyncPIPE)
        stdout, stderr = await fetch.communicate()
        result = stdout.decode().strip() + stderr.decode().strip()
        await e.reply("**" + result + "**")
    except FileNotFoundError:
        await e.reply("**Install speedtest-cli**")

# System information function with disk and memory usage
async def sysinfo(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return
    total, used, free, disk = disk_usage('/')
    memory = virtual_memory()
    await e.reply(
        f"**OS:** {platform.system()}\n"
        f"**Version:** {platform.release()}\n"
        f"**Arch:** {platform.architecture()}\n"
        f"**Total Disk Space:** {hbs(total)}\n"
        f"**Free Disk Space:** {hbs(free)}\n"
        f"**Memory Total:** {hbs(memory.total)}\n"
        f"**Memory Free:** {hbs(memory.available)}\n"
        f"**Memory Used:** {hbs(memory.used)}"
    )

# Function to get video info using mediainfo
async def info(file, e):
    process = subprocess.Popen(
        ["mediainfo", file, "--Output=HTML"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout, _ = process.communicate()
    client = TelegraphPoster(use_api=True)
    client.create_api_token("TGVid-Comp-Mediainfo")
    page = client.post(
        title="TGVid-Comp-Mediainfo",
        author=(await e.client.get_me()).first_name,
        author_url=f"https://t.me/{(await e.client.get_me()).username}",
        text=stdout.decode(),
    )
    return page["url"]

# Queue and Worker management functions
async def skip(e):
    wah = e.pattern_match.group(1).decode("UTF-8")
    wh = decode(wah)
    out, dl, id = wh.split(";")
    try:
        if QUEUE.get(int(id)):
            WORKING.clear()
            QUEUE.pop(int(id))
        await e.delete()
        os.system("rm -rf downloads/*")
        os.system("rm -rf encode/*")
        for proc in psutil.process_iter():
            if proc.name() == "ffmpeg":
                proc.kill()
    except BaseException:
        pass
    return

async def renew(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return
    await e.reply("**Cleared Queued, Working Files and Cached Downloads!**")
    WORKING.clear()
    QUEUE.clear()
    os.system("rm -rf downloads/*")
    os.system("rm -rf encode/*")
    for proc in psutil.process_iter():
        if proc.name() == "ffmpeg":
            proc.kill()
    return

async def coding(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return
    ffmpeg = e.text.split(" ", maxsplit=1)[1]
    ffmpegcode.clear()
    ffmpegcode.insert(0, f"{ffmpeg}")
    await e.reply(f"**Changed FFMPEG Code to**\n\n`{ffmpeg}`")
    return

async def getlogs(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return
    await e.client.send_file(e.chat_id, file=LOG_FILE_NAME, force_document=True)

async def getthumb(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return
    await e.client.send_file(e.chat_id, file="/bot/thumb.jpg", force_document=False, caption="**Your Current Thumbnail.**")

async def getcode(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return
    await e.reply(f"**Your Current FFMPEG Code is**\n\n`{ffmpegcode[0]}`")
    return

async def clearqueue(e):
    if str(e.sender_id) not in OWNER and e.sender_id != DEV:
        return
    await e.reply("**Cleared Queued Files!**")
    QUEUE.clear()
    return

# Fast download function with progress tracking
async def fast_download(e, download_url, filename=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(download_url, timeout=None) as response:
            if not filename:
                filename = download_url.rpartition("/")[-1]
            filename = unquote(filename)
            filename = os.path.join("downloads", filename)
            total_size = int(response.headers.get("content-length", 0)) or None
            downloaded_size = 0
            with open(filename, "wb") as f:
                async for chunk in response.content.iter_chunked(1024):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
            return filename
