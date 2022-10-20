import os
import json
import openpyxl
from setting import STATIC_DIR, STORAGE_DIR


def get_xls_data():
    workbook = openpyxl.load_workbook(os.path.join(STATIC_DIR, "novel.xlsx"))
    # 'Лист1' by default or replace with the desired list
    novel_table = workbook["Лист1"]
    data = {}
    table_keys = ["ru", "choices", "choices_param", "jump_id",
                  "sticker", "photo", "delay", "voice", "event"]
    for row in list(novel_table.rows)[1:]:
        index = str(int(row[0].value))
        data.setdefault(index, {})
        for col in row[1:10]:
            data[index][table_keys[col.col_idx - 2]] = col.value
    if not data:
        raise
    workbook.close()
    return data


def build_checking_args(array: list):
    # Array Example:
    #   ['[0*derzost++1]', '[0*derzost--1]']
    #   ['[0*keks--1&loc==1]', '[0*keks++1&loc==2]', '[0*keks--1&loc==3]', '[0*keks++1&loc==4]']
    # Output Example: {
    #   "check_params": False if 0 else param_name,
    #   "choice_values": [-1, +1]
    # }
    returning_data = {}
    args_array = []
    for lst in array:
        args_list = lst.strip("[]").split("*")
        args_array.append(args_list)
    returning_data["check_params"] = [arg[0] for arg in args_array]
    returning_data["value_setter"] = [arg[1] for arg in args_array]
    # Need thinking about parsing args that will be checked
    # return args_array
    return returning_data


def clear_choices_ids(dialog_data):
    for key in dialog_data.keys():
        choices_field = dialog_data[key]["choices"]
        if choices_field is None:
            continue
        if isinstance(choices_field, str) and "*" in choices_field:
            choices_arr = choices_field.split("*")
            dialog_data[key]["choices"] = list(
                map(lambda x: int(x), choices_arr))
        else:
            dialog_data[key]["choices"] = [int(choices_field)]


def clear_choices_params(dialog_data):
    for key in dialog_data.keys():
        choices_params = dialog_data[key]["choices_param"]
        if choices_params is None:
            continue
        choices_array = choices_params.split(". ")
        dialog_data[key]["choices_param"] = build_checking_args(choices_array)


def main():
    dialog_data = get_xls_data()
    clear_choices_ids(dialog_data)
    clear_choices_params(dialog_data)
    print("")
    with open(f"{STORAGE_DIR}/dialogs.json", mode="w", encoding="utf8") as file:
        file.write(json.dumps(dialog_data, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
