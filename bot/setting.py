import os
import pathlib

BOT_KEY = os.environ.get("BOT_KEY")  # replace with os.environ
BASE_DIR = pathlib.Path(__file__).parent
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
STATIC_DIR = os.path.join(BASE_DIR, "static")
IMAGES_DIR = os.path.join(STATIC_DIR, "img")
MEDIA_DIR = os.path.join(STATIC_DIR, "media")
