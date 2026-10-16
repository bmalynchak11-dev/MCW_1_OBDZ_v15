"""Відкриті приклади 01 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(1)

PUBLIC = [[(['student_id', 'group', 'name', 'phone'],
   [(1, 'A', 'Іваненко', None), (2, 'A', 'Петренко', '067'), (3, 'B', 'Іваненко', '050')]),
  [['student_id'], ['group', 'name']]],
 [(['a', 'b'], [(1, 1), (1, 1)]), []],
 [(['a', 'b'], []), ('ValueError', 'Порожня таблиця')]]

CASES = [tuple(c) for c in PUBLIC]


def _norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [_norm(v) for v in value]
    if isinstance(value, dict):
        return {k: _norm(v) for k, v in value.items()}
    return value


def _check(args, expected):
    fn = getattr(M, "candidate_keys")
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
    assert callable(getattr(M, "candidate_keys", None)), "немає функції candidate_keys"
