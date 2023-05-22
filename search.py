from multiprocessing import Process, Manager
from typing import Optional


def damerau_levenshtein_distance(str1: str, str2: str):
    """
    Вычисляет расстояние Дамерау-Левенштейна между строками
    :param str1: первая строка
    :param str2: вторая строка
    :return: значение расстояния
    """
    matrix = [[0 for _ in range(len(str2) + 1)] for _ in range(len(str1) + 1)]
    # заполняем строки и столбцы индексами
    for i in range(len(str1) + 1):
        matrix[i][0] = i
    for j in range(len(str2) + 1):
        matrix[0][j] = j
    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            # если совпадает, то 0, иначе - 1
            cost = 0 if str1[i - 1] == str2[j - 1] else 1
            # находим минимальную ошибку(deletion, insertion, or substitution)
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j-1] + 1,
                               matrix[i - 1][j-1] + cost)
            # проверяем на переход
            if i > 1 and j > 1 and str1[i - 1] == str2[j - 2] \
                    and str1[i - 2] == str2[j - 1]:
                matrix[i][j] = min(matrix[i][j], matrix[i - 2][j - 2] + cost)
    return matrix[-1][-1]


def search(query, lst, mlist, lock, case_sensitive=True, max_distance=2,
           k_matches=None, reverse=False):
    """
    Производит нечёткий линейный поиск
    :param query: слово для поиска
    :param lst: список слов из текста
    :param mlist: общий словарь процессов
    :param lock: блокировщик для синхронизации процессов
    :param case_sensitive: чувствительность к регистру
    :param max_distance: максимальное расстояние
    :param k_matches: искомое число слов
    :param reverse: проводим ли поиск в обратном порядке
    :return:
    """
    ids = []
    # Loop through the list of strings
    r = range(len(lst) - 1, -1, -1) if reverse else range(len(lst))
    for i in r:
        if not case_sensitive:
            distance = damerau_levenshtein_distance(query.lower(),
                                                    lst[i].lower())
        else:
            distance = damerau_levenshtein_distance(query, lst[i])
        if distance < max_distance:
            ids.append(i)
        if k_matches and len(ids) == k_matches:
            merge_result(mlist, ids, lock)
    merge_result(mlist, ids, lock)


def merge_result(mlist, result, lock):
    """
    Слить результат работы потоков
    :param mlist: общий список процессов
    :param result: результат данного процесса
    :param lock: общий блокировщик для синхронизации процессов
    """
    lock.acquire()
    for item in result:
        mlist.append(item)
    lock.release()


def parallel_search(query, string, case_sensitive=True, max_distance=2,
                    k_matches=None, reverse=False, n_process=None):
    """
    Параллельный поиск подстроки в тексте
    :param query: подстрока для поиска
    :param string: строка, по которой будет осуществляться поиск
    :param case_sensitive: чувствительность к регистру
    :param max_distance: максимальная ошибка
    :param k_matches: искомое количество вхождений
    :param reverse: ищем ли с конца
    :param n_process: количество процессов
    :return:
    """
    manager = Manager()
    mlist = manager.list()
    lock = manager.RLock()
    max_len = 1
    for substring in string:
        size = len(substring)
        if size > max_len:
            max_len = size
    processes = tuple()
    chunk_size = len(string) // (n_process if n_process else 1) + 1
    # Получаем фрагменты строки
    chunks = [string[i:i + chunk_size + max_len - 1]
              for i in range(0, len(string), chunk_size)]
    for chunk in chunks:
        process = Process(
            target=search,
            args=(query, chunk, mlist, lock, case_sensitive,
                  max_distance, k_matches, reverse))
        process.start()
        processes += (process,)
    for process in processes:
        process.join()
    return mlist
