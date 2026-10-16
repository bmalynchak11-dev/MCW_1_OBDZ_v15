"""Відкриті приклади 02 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(2)

PUBLIC = [[('CUSTOMER', 'ORDERS', '0..N', '1..1'),
  "Тип: 1:N\nЗовнішній ключ: ORDERS -> CUSTOMER\nОбов'язковий: так"],
 [('STUDENT', 'COURSE', '0..N', '0..N'),
  "Тип: M:N\nТаблиця зв'язку: STUDENT_COURSE\nПервинний ключ: пара зовнішніх ключів"],
 [('EMPLOYEE', 'PARKING_SPOT', '0..1', '0..1'),
  "Тип: 1:1\nЗовнішній ключ: PARKING_SPOT -> EMPLOYEE\nОбов'язковий: ні\nУнікальність: так"],
 [('A', 'B', '2..N', '1..1'), ('ValueError', 'Некоректна кардинальність')]]

CASES = [tuple(c) for c in PUBLIC]


def _norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [_norm(v) for v in value]
    if isinstance(value, dict):
        return {k: _norm(v) for k, v in value.items()}
    return value


def _check(args, expected):
    fn = getattr(M, "place_fk")
    work = copy.deepcopy(args)
    if isinstance(expected, tuple) and expected and expected[0] == "ValueError":
        with pytest.raises(ValueError) as info:
            fn(*work)
        assert str(info.value) == expected[1]
    else:
        assert _norm(fn(*work)) == _norm(expected)
    assert work == args, "функція не повинна змінювати вхідні дані"


@pytest.mark.parametrize("args,expected", CASES, ids=[f"c{i}" for i in range(len(CASES))])
def test_cases(args, expected):
    _check(args, expected)


def test_function_exists():
    assert callable(getattr(M, "place_fk", None)), "немає функції place_fk"
