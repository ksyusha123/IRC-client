import requests
from PIL import Image, ImageFile


def save_image(link, name):
    image_data = requests.get(link).content
    with open(f'{name}.jpg', 'wb') as f:
        f.write(image_data)


def resize_image(name, width, height):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    image = Image.open(f"{name}.jpg")
    image.thumbnail((width, height))
    image.convert("RGB").save(f"{name}.jpg")
