from argparse import ArgumentParser
from input import print_text, write_to_file, read_from_file
from search import parallel_search


def main():
    """Основная функция программы: точка входа.

    Добавляет и парсит аргументы, после чего вызывает
    функцию поиска и выводит результат

    """
    parser = ArgumentParser()
    parser.add_argument("-s", "--string", type=str, nargs="+", default=None)
    parser.add_argument("-sf", "--source-file", type=str, default=None)
    parser.add_argument("-rf", "--result-file", type=str, default=None)
    parser.add_argument("-ss", "--sub-strings", type=str, nargs="+",
                        required=True)
    parser.add_argument("-cs", "--case-sensitive",
                        action="store_true", default=False)
    parser.add_argument("-r", "--reverse", action="store_true", default=False)
    parser.add_argument("-c", "--count", type=int, default=None)
    parser.add_argument("-t", "--threshold", type=int, default=2)
    parser.add_argument("-p", "--process", type=int, default=None)

    args = parser.parse_args()
    strings = args.string
    result_file = args.result_file
    keys = args.sub_strings
    case_sensitive = args.case_sensitive
    count = args.count
    threshold = args.threshold
    n_process = args.process

    if len(keys) > 5:
        print("The number of keys cant be more than 5")
        return
    if args.source_file:
        if strings:
            print("Error")
            return
        strings = read_from_file(args.source_file)
    if not strings:
        print("No data to search")
        return
    if count and count < 0:
        print("Count can't be negative")
        return
    if threshold < 0:
        print("Threshold can't be negative")
        return
    if n_process and n_process < 0:
        print("Process can't be negative")
        return
    founds = dict()
    ids = dict()
    cnt = 0
    for string in strings:
        words = string.split(" ")
        for key in keys:
            if key not in founds:
                founds[key] = []
            ids[key] = parallel_search(key, words, case_sensitive, threshold,
                                       count, args.reverse)
            for i in ids[key]:
                founds[key].append(words[i])
        print_text(words, ids)
        cnt += 1
        if cnt == 10:
            break
    if result_file:
        write_to_file(result_file, strings, founds)


if __name__ == "__main__":
    main()
