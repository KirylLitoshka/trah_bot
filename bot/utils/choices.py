import re


SIGN_ACTION = {
    "++": lambda a, b: a + b,
    "--": lambda a, b: a - b,
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
}


def on_choice_action(user: dict, choice_expression: str):
    if choice_expression == "0":
        return
    param_name = re.search("[a-z]+", choice_expression).group()
    if param_name in user:
        exp_sign = re.search("[+|-]+", choice_expression).group()
        exp_value = re.search("[0-9]+", choice_expression).group()
        user[param_name] = SIGN_ACTION[exp_sign](user[param_name], int(exp_value))
    else:
        raise Exception(f"User doesn't have '{param_name}' param")


def check_args(user, expression):
    if expression == "0":
        return True
    param_name = re.search("[a-z]+", expression).group()
    if param_name in user:
        exp_sign = re.search("[=|<|>]+", expression).group()
        exp_value = re.search("[0-9]+", expression).group()
        return SIGN_ACTION[exp_sign](user[param_name], int(exp_value))
    else:
        raise Exception(f"User doesn't have '{param_name}' param")

