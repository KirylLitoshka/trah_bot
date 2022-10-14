from openpyxl import load_workbook
from setting import STORAGE_DIR


def get_data_from_excel(file_name: str):
    data = {}
    workbook = load_workbook(f"{STORAGE_DIR}/{file_name}")
    novel_table = workbook["Лист1"]
    table_keys = ["ru", "choices", "choices_param", "jump_id", "sticker", "photo", "delay", "voice", "event"]
    for row in list(novel_table.rows)[1:]:
        index = str(row[0].value)
        data.setdefault(index, {})
        for col in row[1:10]:
            data[index][table_keys[col.col_idx - 2]] = col.value
    if not data:
        raise
    return data
            
