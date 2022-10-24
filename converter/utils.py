import openpyxl
from contextlib import contextmanager


@contextmanager
def open_workbook(*args, **kwargs):
    workbook = openpyxl.load_workbook(*args, **kwargs)
    try:
        yield workbook
    finally:
        workbook.close()


def clean_choices(value):
    if value is None:
        return None
    return str(value).split("*")


def clean_jump_id(value):
    if value is None:
        return None
    return str(value)


def clean_choices_param(value):
    if value is None:
        return None
    params_array = value.split(". ")
    output_array = []
    for param in params_array:
        choices = param.strip("][").split("*")
        param_value = {"check_args": choices[0], "on_choice": choices[1]}
        output_array.append(param_value)
    return output_array


def clean_item(item: dict) -> None:
    item["choices"] = clean_choices(item["choices"])
    item["jump_id"] = clean_jump_id(item["jump_id"])
    item["choices_param"] = clean_choices_param(item["choices_param"])


def clean_data(data: dict) -> dict:
    for key in data.keys():
        clean_item(data[key])
    return data


def excel_as_dict(fn):
    table_keys = [
        "text",
        "choices",
        "choices_param",
        "jump_id",
        "sticker",
        "photo",
        "delay",
        "voice",
        "event",
    ]

    def wrapper(*args, **kwargs):
        xls_data = fn(*args, **kwargs)
        data = {}
        for worksheet_row in list(xls_data.rows)[1:]:
            dialog_id = str(int(worksheet_row[0].value))
            data[dialog_id] = {}
            for col in worksheet_row[1:10]:
                data[dialog_id][table_keys[col.col_idx - 2]] = col.value
        if not data:
            raise
        return clean_data(data)

    return wrapper
