def natural_join(
    r_attrs: list,
    r_rows: list,
    s_attrs: list,
    s_rows: list,
    outer: bool = False,
) -> tuple:
    # 1. Перевірка повторення атрибутів
    seen_r = set()
    for a in r_attrs:
        if a in seen_r:
            raise ValueError(f"Повторення атрибута: {a}")
        seen_r.add(a)

    seen_s = set()
    for a in s_attrs:
        if a in seen_s:
            raise ValueError(f"Повторення атрибута: {a}")
        seen_s.add(a)

    # 2. Перевірка довжини кортежів
    len_r = len(r_attrs)
    for r in r_rows:
        if len(r) != len_r:
            raise ValueError("Некоректний кортеж")

    len_s = len(s_attrs)
    for s in s_rows:
        if len(s) != len_s:
            raise ValueError("Некоректний кортеж")

    # Спільні атрибути та додаткові атрибути відношення S
    common_attrs = [a for a in r_attrs if a in seen_s]
    s_extra_attrs = [a for a in s_attrs if a not in seen_r]

    out_attrs = list(r_attrs) + s_extra_attrs

    r_common_idx = [r_attrs.index(a) for a in common_attrs]
    s_common_idx = [s_attrs.index(a) for a in common_attrs]
    s_extra_idx = [s_attrs.index(a) for a in s_extra_attrs]

    result_rows = []
    seen_result = set()

    for r in r_rows:
        matched = False
        for s in s_rows:
            # З'єднання можливе лише якщо жодне спільне поле не є None і всі значення рівні
            match = True
            for ri, si in zip(r_common_idx, s_common_idx):
                if r[ri] is None or s[si] is None or r[ri] != s[si]:
                    match = False
                    break

            if match:
                matched = True
                combined = tuple(r) + tuple(s[i] for i in s_extra_idx)
                if combined not in seen_result:
                    seen_result.add(combined)
                    result_rows.append(combined)

        if outer and not matched:
            combined = tuple(r) + tuple(None for _ in s_extra_idx)
            if combined not in seen_result:
                seen_result.add(combined)
                result_rows.append(combined)

    return (out_attrs, result_rows)