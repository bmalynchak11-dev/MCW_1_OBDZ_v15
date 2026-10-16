"""Відкриті приклади 07 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(7)

PUBLIC = [[('A B C D', ['A B -> C', 'B -> D']),
  'Ключі: {A, B}\nПервинні атрибути: A, B\nФорма: 1NF\nПорушення:\n- 2NF: {B} -> {D}'],
 [('A B C', ['A -> B', 'B -> C']),
  'Ключі: {A}\nПервинні атрибути: A\nФорма: 2NF\nПорушення:\n- 3NF: {B} -> {C}'],
 [('student subject teacher', ['student subject -> teacher', 'teacher -> subject']),
  'Ключі: {student, subject}; {student, teacher}\n'
  'Первинні атрибути: student, subject, teacher\n'
  'Форма: 3NF\n'
  'Порушення:\n'
  '- BCNF: {teacher} -> {subject}'],
 [('A B', ['A -> C']), ('ValueError', 'Невідомий атрибут: C')]]

CASES = [tuple(c) for c in PUBLIC]


def _norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [_norm(v) for v in value]
    if isinstance(value, dict):
        return {k: _norm(v) for k, v in value.items()}
    return value


def _check(args, expected):
    fn = getattr(M, "normal_form_report")
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
    assert callable(getattr(M, "normal_form_report", None)), "немає функції normal_form_report"
