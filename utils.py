import copy
from typing import List

from sqlalchemy import true


def readFile(filename):
    fo = open(filename, "r")
    print("read require file: ", fo.name)

    list: List[str] = []

    for line in fo.readlines():
        line = line.strip()
        list.append(copy.copy(line))

    fo.close()

    return list


def isInfoStart(i: str):
    if i == '[' or i == '【' or i == '［':
        return True
    else:
        return False


def isInfoEnd(i: str):
    if i == ']' or i == '】' or i == '］':
        return True
    else:
        return False


def isDataStart(i: str):
    if i == '(' or i == '（':
        return True
    else:
        return False


def isDataEnd(i: str):
    if i == ')' or i == '）':
        return True
    else:
        return False
