"""Відкриті приклади 03 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(3)

PUBLIC = [[(['group', 'teacher', 'room'],
   [('K1', 'Коваль', '101'), ('K1', 'Коваль', '102'), ('K2', 'Мельник', '101')],
   ['group'],
   ['teacher']),
  'Залежність group -> teacher виконується'],
 [(['group', 'teacher', 'room'],
   [('K1', 'Коваль', '101'), ('K1', 'Коваль', '102'), ('K2', 'Мельник', '101')],
   ['group'],
   ['room']),
  'Залежність group -> room не виконується\n'
  'Перше порушення: рядки 1 і 2\n'
  'Пар, що порушують: 1'],
 [(['group', 'teacher', 'room'],
   [('K1', 'Коваль', '101'), ('K1', 'Коваль', '102'), ('K2', 'Мельник', '101')],
   ['group'],
   ['floor']),
  ('ValueError', 'Невідомий стовпець: floor')]]

CASES = [tuple(c) for c in PUBLIC]


def _norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [_norm(v) for v in value]
    if isinstance(value, dict):
        return {k: _norm(v) for k, v in value.items()}
    return value


def _check(args, expected):
    fn = getattr(M, "check_fd")
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
    assert callable(getattr(M, "check_fd", None)), "немає функції check_fd"
