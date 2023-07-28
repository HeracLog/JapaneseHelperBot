import requests
from tqdm import tqdm
from io import BytesIO
from PIL import Image
import os

# Function to download the images
def downloadImages():
    # Opens the file and formats it properly
    linksFile = open("imgs.txt","r")
    linksText = linksFile.read()
    # Removes all single quotes
    linksText = linksText.replace("'","")
    linksText = linksText.replace("]","")
    linksText = linksText.replace("[","")
    # Splits the text at ,
    links : list = linksText.split(",")

    # Tries to create a directory for the images
    try:
        os.mkdir("./JapaneseImgs")
    except:
        print("Directory exists")

    # Starts a new session for fetching the images
    session : requests.Session = requests.session()
    # Loops through all images
    for i in tqdm(range(0,len(links)), desc="Downloading images"):
        # Tries to get the images
        try:
            # Stores the response
            response = session.get(links[i])

            # If the response is OK we continue
            if response.status_code == 200:
                # Reads the bytes from the response
                image_content = BytesIO(response.content)
                # Opens the image and converts it into RGB
                image = Image.open(image_content)
                image = image.convert("RGB")
                # Saves the image and thats pretty much it
                image.save(f"./JapaneseImgs/{i}.jpg")
            # If the response isnt OK we log the status code
            else:
                print(response.status_code)
        # If an exception occur we log it out
        except Exception as e:
            print(f"Something went wrong with {i}", e)