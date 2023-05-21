import os
from colorama import init, Back, Fore, Style
from typing import Union


def read_from_file(file_name=None) -> str:
    """
    Считывание строк из файла
    :param file_name: имя файла для открытия
    :return: считанная строка или None
    """
    while not file_name:
        file_name = input("Please, enter a file name (with extension): ")
        if not os.path.exists(file_name):
            print("This filename is incorrect. Please, try again")
            file_name = None
    string = ""
    counter = 0
    with open(file_name, "r", encoding='utf-8') as file:
        for line in file:
            string += line
            counter += 1
            if counter > 10:
                break
    if (not string) or (string == " "):
        print("Read string is empty")
        string = None
    else:
        string = ' '.join(string.split("\n"))
    return string


def create_one_key(found: Union[tuple, None], key: str) -> list:
    """
    Создание массива индексов для одного ключа
    :param found: индексы найденных ключевых слов
    :param key: название искомого ключа
    :return: массива индексов
    """
    ids = []
    for i in range(len(found)):
        ids.append([])
        for j in range(len(key)):
            ids[i].append(found[i] + j)
    return ids


def print_text(string: str, found: Union[tuple, None],
               key: str) -> None:
    """
    Цветной вывод найденных подстрок в консоль
    :param string: строка для поиска
    :param found: индексы найденных ключевых слов
    :param key: ключевые слова
    :return: None
    """
    if not found:
        "There are no substrings founded here"
        print(string)
    else:
        if isinstance(found, tuple):
            found = create_one_key(found, key)
        init()
        color_id = 0
        colors = (
            Style.BRIGHT + Fore.BLUE + Back.RED,
            Style.BRIGHT + Fore.CYAN + Back.YELLOW,
            Style.BRIGHT + Fore.YELLOW + Back.CYAN,
            Style.BRIGHT + Fore.MAGENTA + Back.GREEN,
            Style.BRIGHT + Fore.GREEN + Back.MAGENTA,
        )
        reset = Style.RESET_ALL + Fore.RESET + Back.RESET
        counter = 0
        for i, char in enumerate(string):
            if i in found[counter]:
                print(colors[color_id] + char, end="")
            elif counter + 1 < len(found) and i in found[counter + 1]:
                counter += 1
                if color_id + 1 == len(colors):
                    color_id = 0
                else:
                    color_id += 1
                print(colors[color_id] + char, end="")
            else:
                print(reset + char, end="")
        print(Back.RESET)
