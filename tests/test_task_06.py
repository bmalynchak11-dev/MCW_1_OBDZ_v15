"""Відкриті приклади 06 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(6)

PUBLIC = [[({'entities': {'CUSTOMER': {'attrs': ['name', 'email']},
                 'ORDERS': {'attrs': ['created_on']},
                 'PRODUCT': {'attrs': ['title']}},
    'relationships': [{'name': 'PLACES',
                       'a': 'CUSTOMER',
                       'b': 'ORDERS',
                       'a_to_b': '0..N',
                       'b_to_a': '1..1',
                       'attrs': []},
                      {'name': 'CONTAINS',
                       'a': 'ORDERS',
                       'b': 'PRODUCT',
                       'a_to_b': '1..N',
                       'b_to_a': '0..N',
                       'attrs': ['qty']}]},),
  {'customer': {'columns': ['id', 'name', 'email'], 'pk': ['id'], 'fks': [], 'unique': []},
   'orders': {'columns': ['id', 'created_on', 'customer_id'],
              'pk': ['id'],
              'fks': [{'column': 'customer_id',
                       'ref': 'customer',
                       'required': True,
                       'cascade': False}],
              'unique': []},
   'product': {'columns': ['id', 'title'], 'pk': ['id'], 'fks': [], 'unique': []},
   'contains': {'columns': ['orders_id', 'product_id', 'qty'],
                'pk': ['orders_id', 'product_id'],
                'fks': [{'column': 'orders_id',
                         'ref': 'orders',
                         'required': True,
                         'cascade': True},
                        {'column': 'product_id',
                         'ref': 'product',
                         'required': True,
                         'cascade': True}],
                'unique': []}}],
 [({'entities': {'ORDERS': {'attrs': ['created_on']},
                 'ORDER_LINE': {'owner': 'ORDERS',
                                'key': ['line_no'],
                                'attrs': ['qty', 'price']}},
    'relationships': []},),
  {'orders': {'columns': ['id', 'created_on'], 'pk': ['id'], 'fks': [], 'unique': []},
   'order_line': {'columns': ['orders_id', 'line_no', 'qty', 'price'],
                  'pk': ['orders_id', 'line_no'],
                  'fks': [{'column': 'orders_id',
                           'ref': 'orders',
                           'required': True,
                           'cascade': True}],
                  'unique': []}}],
 [({'entities': {'A': {'attrs': []}},
    'relationships': [{'name': 'R',
                       'a': 'A',
                       'b': 'Z',
                       'a_to_b': '0..N',
                       'b_to_a': '0..N',
                       'attrs': []}]},),
  ('ValueError', 'Невідома сутність: Z')]]

CASES = [tuple(c) for c in PUBLIC]


def _norm(value):
    """Кортежі й списки порівнюються однаково."""
    if isinstance(value, (list, tuple)):
        return [_norm(v) for v in value]
    if isinstance(value, dict):
        return {k: _norm(v) for k, v in value.items()}
    return value


def _check(args, expected):
    fn = getattr(M, "er_to_tables")
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
    assert callable(getattr(M, "er_to_tables", None)), "немає функції er_to_tables"
