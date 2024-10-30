# https://github.com/1Danish-00/CompressorQueue/blob/main/License> .
from fastapi import FastAPI
import logging
import asyncio
import glob
import inspect
import io
import itertools
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import traceback
from datetime import datetime as dt
from logging import DEBUG, INFO, basicConfig, getLogger, warning
from logging.handlers import RotatingFileHandler
from pathlib import Path
import aiohttp
import psutil
from html_telegraph_poster import TelegraphPoster
from telethon import Button, TelegramClient, errors, events, functions, types
from telethon.sessions import StringSession
from telethon.utils import pack_bot_file_id
from .config import *
LOG_FILE_NAME = "TGVid-Comp@Log.txt"


# Clear the log file if it exists
if os.path.exists(LOG_FILE_NAME):
    with open(LOG_FILE_NAME, "r+") as f_d:
        f_d.truncate(0)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=2097152000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("FastTelethon").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
LOGS = logging.getLogger(__name__)

# Initialize the Telegram bot
try:
    bot = TelegramClient(None, APP_ID, API_HASH)  # No session required
except Exception as e:
    LOGS.error("Environment vars are missing! Kindly recheck.")
    LOGS.error(str(e))
    exit()

# Dummy FastAPI server
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bot is running"}

# Start the bot asynchronously
async def start_bot():
    await bot.start()
    LOGS.info("Bot has started and is listening for commands...")

if __name__ == "__main__":
    import uvicorn

    # Start the bot in a background task
    asyncio.run(start_bot())

    # Start the FastAPI server to bind to a port
    host = os.getenv("HOST", "0.0.0.0")  # Default host to '0.0.0.0' if HOST not set
    port = int(os.getenv("PORT", 8000))  # Default port to 8000 if PORT not set
    uvicorn.run(app, host=host, port=port)
