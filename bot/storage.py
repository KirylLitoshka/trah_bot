import aiofiles
import json
from setting import STORAGE_DIR


async def load_data(file_name: str):
    async with aiofiles.open(f"{STORAGE_DIR}/{file_name}.json", encoding="utf8") as fp:
        file_data = await fp.read()
        return json.loads(file_data)


async def save_data(file_name: str, data: dict):
    async with aiofiles.open(
        f"{STORAGE_DIR}/{file_name}.json", mode="w", encoding="utf8"
    ) as fp:
        saving_data = json.dumps(data, ensure_ascii=False)
        await fp.write(saving_data)
