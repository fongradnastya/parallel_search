import os
from colorama import init, Back, Fore, Style
from typing import Union


def read_from_file(file_name: str) -> list:
    """
    Считывание строк из файла
    :param file_name: имя файла для открытия
    :return:
    """
    strings = []
    with open(file_name, "r", encoding='utf-8') as file:
        for line in file:
            strings.append(line.strip("\n"))
    if not strings:
        print("Read string is empty")
    return strings


def write_to_file(result_file, strings, ids):
    try:
        rfile = open(result_file, "w", encoding="utf-8")
        rfile.close()
    except PermissionError:
        print("Unable to open result file")
        return
    file = open(result_file, "a", encoding="utf-8")
    file.write("data: '" + " ".join(strings) + "'\n")
    file.write("Results:\n")
    for key in ids:
        file.write(key + ": ")
        for i in ids[key]:
            file.write(strings[i] + " ")
        file.write("\n")
    file.close()


def print_colored_word(word, color, reset):
    for char in word:
        print(color + char, end="")
    print(reset + " ", end="")


def print_text(strings: list, found: Union[dict, None]) -> None:
    """
    Цветной вывод найденных подстрок в консоль
    :param string: строка для поиска
    :param found: индексы найденных ключевых слов
    :param key: ключевые слова
    :return: None
    """
    if not found:
        "There are no substrings founded here"
        print(" ".join(strings))
    else:
        init()
        colors = (
            Style.BRIGHT + Fore.BLACK + Back.RED,
            Style.BRIGHT + Fore.BLACK + Back.YELLOW,
            Style.BRIGHT + Fore.BLACK + Back.CYAN,
            Style.BRIGHT + Fore.BLACK + Back.GREEN,
            Style.BRIGHT + Fore.BLACK + Back.MAGENTA,
        )
        keys = list(found.keys())
        reset = Style.RESET_ALL + Fore.RESET + Back.RESET
        for i in range(len(strings)):
            for j in range(len(keys)):
                if i in found[keys[j]]:
                    color = colors[j]
                    print_colored_word(strings[i], color, reset)
                    break
            else:
                print(reset + strings[i], end=" ")
        print(Back.RESET)
