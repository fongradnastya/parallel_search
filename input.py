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


def print_colored_word(word, color, reset):
    for char in word:
        print(color + char, end="")
    print(reset + " ", end="")


def print_text(strings: list, found: Union[list, None]) -> None:
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
        color_id = 0
        colors = (
            Style.BRIGHT + Fore.BLACK + Back.RED,
            Style.BRIGHT + Fore.BLACK + Back.YELLOW,
            Style.BRIGHT + Fore.BLACK + Back.CYAN,
            Style.BRIGHT + Fore.BLACK + Back.GREEN,
            Style.BRIGHT + Fore.BLACK + Back.MAGENTA,
        )
        reset = Style.RESET_ALL + Fore.RESET + Back.RESET
        for i in range(len(strings)):
            if i in found:
                print_colored_word(strings[i], colors[color_id], reset)
                if color_id + 1 == len(colors):
                    color_id = 0
                else:
                    color_id += 1
            else:
                print(reset + strings[i], end=" ")
        print(Back.RESET)
