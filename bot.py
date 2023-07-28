import os
import sys
import random
import asyncio
from telegram import InputFile, Update
from telegram.ext import Application, CommandHandler, ContextTypes


# You put the bot api token here
# You get it from botfather on telegram
BOT_TOKEN : str = ""

# Put the bot username here
# Wont really affect anything
username : str = "BotName"
# Fetches all images in the directory we downloaded the images to
images : list = [img for img in os.listdir("./JapaneseImgs") if img.endswith(".jpg")]
# Shuffles because yes
random.shuffle(images)

# Function that sends the images
async def sendImages(update : Update, context : ContextTypes.DEFAULT_TYPE):
    # Tries to send the images
    try:
        # Gets the username of the user texting it
        name : str = update.message.chat.full_name
        # Loops for pretty much the end of time
        while True:
            # Logs and send an alert to the user
            print("Will send an image now")
            await update.message.reply_text("Sending image now")
            # Pops the image at the front of a list and adds it to the back
            # Like a FIFO system in a queue
            # No it is literally that 
            image = images.pop(0)
            images.append(image)
            # Joins paths with the directory
            image = os.path.join("./JapaneseImgs", image)
            # Opens the image in read binary mode
            with open(image,"rb") as f:
                # Gets the image to send
                imageToSend = InputFile(f)
                # gets the size of the image so we can calulate the timeout
                size = os.path.getsize(image) / (1024**2)
                # Time out it N times the size of the file and we add 15 seconds overhead
                timeout = (size / (1/8)) + 15
            # Sends the image
            await update.message.reply_photo(imageToSend, read_timeout=timeout, write_timeout=timeout)
            # Logs out the event
            print(f"{username} sent an image to {name}")
            # Sleeps for a day
            await asyncio.sleep(24*60*60)
    # In case of an exception we log it out
    except Exception as e:
        print("Oopsie ", e)

# Error handeller, dont worry about it
async def error(update :Update, context : ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused {context.error}", file=sys.stderr)

if __name__ == "__main__":
    # Starts bot
    print("Starting bot")
    app = Application.builder().token(BOT_TOKEN).build()

    # Adds the handlers and starts polling
    app.add_handler(CommandHandler("start",sendImages))
    app.add_error_handler(error)
    print("Started polling")
    app.run_polling()