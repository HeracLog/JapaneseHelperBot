import os
import sys
import random
import asyncio
from telegram import InputFile, Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN : str = ""

username : str = "JapaneseHelper"
images : list = [img for img in os.listdir("./JapaneseImgs") if img.endswith(".jpg")]
random.shuffle(images)


async def sendImages(update : Update, context : ContextTypes.DEFAULT_TYPE):
    try:
        name : str = update.message.chat.full_name
        while True:
            print("Will send an image now")
            await update.message.reply_text("Sending image now")
            image = images.pop(0)
            images.append(image)
            image = os.path.join("./JapaneseImgs", image)
            with open(image,"rb") as f:
                imageToSend = InputFile(f)
                size = os.path.getsize(image) / (1024**2)
                timeout = (size / (1/8)) + 15
            await update.message.reply_photo(imageToSend, read_timeout=timeout, write_timeout=timeout)
            print(f"{username} sent an image to {name}")
            await asyncio.sleep(3)
    except Exception as e:
        print("Oopsie ", e)

async def error(update :Update, context : ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused {context.error}", file=sys.stderr)

if __name__ == "__main__":
    print("Starting bot")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",sendImages))
    app.add_error_handler(error)
    print("Started polling")
    app.run_polling()