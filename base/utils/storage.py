import json


def load_data(dir: str, file_name: str):
    with open(f"{dir}/{file_name}.json", encoding="utf8") as fp:
        file_data = fp.read()
        return json.loads(file_data)


def save_data(dir: str, file_name: str, data: dict):
    with open(f"{dir}/{file_name}.json", mode="w", encoding="utf8") as fp:
        saving_data = json.dumps(data, ensure_ascii=False, indent=4)
        fp.write(saving_data)
