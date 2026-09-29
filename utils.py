import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')

def isNumordot(string: str):
    return string.isdigit() or string == '.'

def isValidNumber(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        print('deu ruim')
        valid = False
    return valid


def isEmpty(string: str):
    return len(string) == 0
