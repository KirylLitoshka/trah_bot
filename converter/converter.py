import json
import os
import pathlib
from utils import open_workbook, excel_as_dict

CONV_PATH = pathlib.Path(__file__).parent


@excel_as_dict
def get_data(file_name=None):
    if file_name is None:
        file_name = "novel.xlsx"
    with open_workbook(os.path.join(CONV_PATH, file_name)) as workbook:
        workbook_list_name = "Лист1"
        novel_table = workbook[workbook_list_name]
    return novel_table


def write_data(data, file_name=None):
    if file_name is None:
        file_name = "dialogs.json"
    with open(os.path.join(CONV_PATH, file_name), "w", encoding="utf8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))


def main():
    dialog_data = get_data()
    write_data(dialog_data)


if __name__ == "__main__":
    main()
