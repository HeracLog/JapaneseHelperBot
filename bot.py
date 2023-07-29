from datetime import datetime
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
username : str = ""
# Fetches all images in the directory we downloaded the images to
images : list = [img for img in os.listdir("./JapaneseImgs") if img.endswith(".jpg")]
# Shuffles because yes
random.shuffle(images)

# Last time an image was sent
lastSend : datetime= datetime.now()

# Function that sends the images
async def sendImages(update : Update, context : ContextTypes.DEFAULT_TYPE):
    # Tries to send the images
    try:
        # Gets the username of the user texting it
        name : str = update.message.chat.full_name
        # Loops for pretty much the end of time
        while True:
            # Runs the loop until we stop it
            try:
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
                # Sets lastSend as current time
                global lastSend
                lastSend = datetime.now()
                # Sleeps for a day
                await asyncio.sleep(24*60*60)
            # If the task is canceled we will break out of the function
            except asyncio.CancelledError:
                print("Stopping")
                break
    # In case of an exception we log it out
    except Exception as e:
        print("Oopsie ", e)

async def start(update : Update, context : ContextTypes.DEFAULT_TYPE):
    # Starts an async function as a task and we set its name so we can know it
    task = asyncio.create_task(sendImages(update,context))
    task.set_name("SendImages")

async def status(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I am alive don't worry :>")
    # Gets current time
    checkUpTime :datetime = datetime.now()
    # Subtracts the difference between now and last send
    difference = checkUpTime - lastSend
    # Gets the horus by dividing the seconds by 3600
    hour : int = difference.seconds // 3600
    # Gets the minutes by finding the remainder and dividing it by 60
    minute : int = (difference.seconds % 3600) // 60
    # Finally the seconds are the remainder of 60
    sec : int = difference.seconds % 60
    # Replies with the time
    await update.message.reply_text(f"Last send was {hour}hrs:{minute}mins:{sec}secs ago")

async def stop(update : Update, context : ContextTypes.DEFAULT_TYPE):
    # Gets all running async tasks
    tasks = asyncio.all_tasks()
    # Loops thorugh each task
    for task in tasks:
        # If we found the task we cancel it
        if task.get_name() == "SendImages":
            task.cancel()
    # Log and send the message to the user
    await update.message.reply_text("Stopping byeee")
    print("stopped")
# Error handeller, dont worry about it
async def error(update :Update, context : ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused {context.error}", file=sys.stderr)

if __name__ == "__main__":
    # Starts bot
    print("Starting bot")
    app = Application.builder().token(BOT_TOKEN).build()

    # Adds the handlers and starts polling
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("stop",stop))
    app.add_handler(CommandHandler("status",status))
    app.add_error_handler(error)
    print("Started polling")
    app.run_polling()

    # Starts the main event loop
    loop = asyncio.get_event_loop()
    # We run it forever and if an exception occurs it frees the memeory its holding
    try:
        loop.run_forever()
    finally:
        # Runs regardless of what happens above at the end of the application
        loop.close()