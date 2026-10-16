"""Відкриті приклади 09 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(9)

PUBLIC = [[('student subject teacher', ['student subject -> teacher', 'teacher -> subject']),
  {'relations': [['student', 'teacher'], ['subject', 'teacher']],
   'lost': ['student subject -> teacher']}],
 [('A B C D', ['A -> B', 'B -> C', 'C -> D']),
  {'relations': [['A', 'B'], ['B', 'C'], ['C', 'D']], 'lost': []}],
 [('A B', ['A -> Z']), ('ValueError', 'Невідомий атрибут: Z')]]

CASES = [tuple(c) for c in PUBLIC]


def _norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [_norm(v) for v in value]
    if isinstance(value, dict):
        return {k: _norm(v) for k, v in value.items()}
    return value


def _check(args, expected):
    fn = getattr(M, "bcnf_decompose")
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
    assert callable(getattr(M, "bcnf_decompose", None)), "немає функції bcnf_decompose"
