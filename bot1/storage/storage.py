import json
from setting import STORAGE_DIR


def load_data(file_name: str):
    with open(f"{STORAGE_DIR}/{file_name}.json", encoding="utf8") as fp:
        file_data = fp.read()
        return json.loads(file_data)


def save_data(file_name: str, data: dict):
    with open(f"{STORAGE_DIR}/{file_name}.json", mode="w", encoding="utf8") as fp:
        saving_data = json.dumps(data, ensure_ascii=False, indent=4)
        fp.write(saving_data)
