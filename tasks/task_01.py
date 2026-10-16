from itertools import combinations


def candidate_keys(columns: list, rows: list) -> list:
    # 1. Перевірка коректності структури
    if not columns or len(set(columns)) != len(columns):
        raise ValueError("Некоректні дані")

    col_count = len(columns)
    for row in rows:
        if len(row) != col_count:
            raise ValueError("Некоректні дані")

    # 2. Перевірка на порожню таблицю
    if len(rows) == 0:
        raise ValueError("Порожня таблиця")

    n = len(rows)
    superkeys = []
    col_indices = list(range(col_count))

    # Пошук надключів: перебір комбінацій індексів за зростанням довжини
    for r in range(1, col_count + 1):
        for combo in combinations(col_indices, r):
            # Перевірка: жодне значення в комбінації не має бути None
            has_none = False
            for row in rows:
                if any(row[i] is None for i in combo):
                    has_none = True
                    break
            if has_none:
                continue

            # Перевірка унікальності комбінацій
            unique_tuples = {tuple(row[i] for i in combo) for row in rows}
            if len(unique_tuples) == n:
                superkeys.append(set(combo))

    # Відбір мінімальних надключів (потенційних ключів)
    cand_keys_sets = []
    for sk in superkeys:
        if not any(other < sk for other in superkeys):
            if sk not in cand_keys_sets:
                cand_keys_sets.append(sk)

    # Формування результату зі збереженням вихідного порядку стовпців
    result = []
    for k_set in cand_keys_sets:
        ordered_key = [columns[i] for i in sorted(k_set)]
        result.append(ordered_key)

    # Сортування ключів: за розміром, потім лексикографічно за позиціями в columns
    def sort_key(k):
        indices = [columns.index(col) for col in k]
        return (len(indices), indices)

    result.sort(key=sort_key)
    return result