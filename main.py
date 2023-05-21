from argparse import ArgumentParser
from input import print_text
from search import search


def main():
    """Основная функция программы: точка входа.

    Добавляет и парсит аргументы, после чего вызывает
    функцию поиска и выводит результат

    """
    parser = ArgumentParser()
    parser.add_argument("-s", "--string", type=str, nargs="+", required=True)
    parser.add_argument("-f", "--file", action="store_true", default=False)
    parser.add_argument("-rf", "--result-file", type=str, default=None)
    parser.add_argument("-ss", "--sub-string", type=str, required=True)
    parser.add_argument("-cs", "--case-sensitive",
                        action="store_true", default=False)
    parser.add_argument("-r", "--reverse", action="store_true", default=False)
    parser.add_argument("-c", "--count", type=int, default=None)
    parser.add_argument("-t", "--threshold", type=int, default=1)
    parser.add_argument("-p", "--process", type=int, default=None)

    args = parser.parse_args()
    strings = args.string
    print(strings)
    file_flag = args.file
    result_file = args.result_file
    substring = args.sub_string
    case_sensitive = args.case_sensitive
    count = args.count
    threshold = args.threshold
    n_process = args.process

    if len(strings) > 10:
        print("The number of strings cant be more than 10")
        return
    if file_flag:
        if len(strings) > 1:
            print("Can't be specified the path to more than one file")
            return
        try:
            file = open(strings[0], "r", encoding="utf-8")
        except FileNotFoundError:
            print("The file not found")
            return
        else:
            strings = ("".join(file.readlines()),)
        finally:
            file.close()
    if count and count < 0:
        print("Count cant be negative")
        return
    if threshold < 0:
        print("Threshold cant be negative")
        return
    if n_process and n_process < 0:
        print("Process cant be negative")
        return

    if result_file:
        try:
            rfile = open(result_file, "w", encoding="utf-8")
        except PermissionError:
            print("Unable to open result file")
            return

    match = search(substring, strings, case_sensitive, threshold, count,
                   args.reverse)
    print(f"The closest match to {substring} is {match}")
    if result_file:
        rfile.close()


if __name__ == "__main__":
    main()
