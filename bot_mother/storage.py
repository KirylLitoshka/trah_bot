import json

from bot_mother.settings import STORAGE_DIR


def set_users(dispatcher):
    with open(f"{STORAGE_DIR}/users.json", mode="r", encoding="utf8") as user_storage:
        users_data = json.loads(user_storage.read())
    dispatcher.data['users'] = users_data
    
