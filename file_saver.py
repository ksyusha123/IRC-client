import requests
from PIL import Image
import os


def save_image(link, name):
    if not os.path.isdir(".pictures"):
        os.mkdir(".pictures")
    image_data = requests.get(link).content
    with open(f'{name}.jpg', 'wb') as f:
        f.write(image_data)
    os.replace(f'{name}.jpg', f'.pictures/{name}.jpg')


def resize_image(name, width, height):
    image = Image.open(f".pictures/{name}.jpg")
    image.thumbnail((width, height))
    image.convert("RGB").save(f".pictures/{name}.jpg")
