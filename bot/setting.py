import os
import pathlib

BOT_KEY = "5585358026:AAFZ_MdfbBW70b2Ds9QdtqBXfLmHI1cjBb4"  # replace with os.environ
BASE_DIR = pathlib.Path(__file__).parent
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
STATIC_DIR = os.path.join(BASE_DIR, "static")
IMAGES_DIR = os.path.join(STATIC_DIR, "img")
