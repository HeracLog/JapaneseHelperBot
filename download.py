import requests
from tqdm import tqdm
from io import BytesIO
from PIL import Image
import os

def downloadImages():
    linksFile = open("imgs.txt","r")
    linksText = linksFile.read()
    linksText = linksText.replace("'","")
    links : list = linksText.split(",")

    try:
        os.mkdir("./JapaneseImgs")
    except:
        print("Directory exists")

    session : requests.Session = requests.session()
    for i in tqdm(range(0,len(links)), desc="Downloading images"):
        try:
            response = session.get(links[i])

            if response.status_code == 200:
                image_content = BytesIO(response.content)
                image = Image.open(image_content)
                image = image.convert("RGB")
                image.save(f"./JapaneseImgs/{i}.jpg")
            else:
                print(response.status_code)
        except Exception as e:
            print(f"Something went wrong with {i}", e)