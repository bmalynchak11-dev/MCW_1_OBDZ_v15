"""Відкриті приклади 04 (з картки). Повний набір перевірок — у викладача."""
import pytest
from conftest import load
from pgutil import attempt, columns, constraints, canon

M = load(4)


@pytest.fixture
def created(db):
    sql = M.create_script()
    assert isinstance(sql, str), "create_script() має повертати рядок з SQL"
    db.run(sql)
    return db


def test_columns(created):
    cols = columns(created, "membership")
    assert list(cols) == ["id", "member_name", "email", "plan", "started_on", "ends_on", "price"]
    expected = {"id": "integer", "member_name": "character varying(100)", "email": "character varying(120)",
                "plan": "character varying(10)", "started_on": "date", "ends_on": "date", "price": "numeric(8,2)"}
    assert {k: v["type"] for k, v in cols.items()} == expected
    assert cols["id"]["identity"] == "a", "id має бути GENERATED ALWAYS AS IDENTITY"


def test_primary_key_and_unique(created):
    cons = constraints(created, "membership")
    assert any(c["type"] == "p" and c["cols"] == ["id"] for c in cons)
    assert any(c["type"] == "u" and c["cols"] == ["email"] for c in cons)


def test_valid_row_and_defaults(created):
    created.run("INSERT INTO membership (member_name, ends_on, price) VALUES ('Іваненко', current_date + 30, 450)")
    assert created.rows("SELECT plan, started_on = current_date FROM membership") == [("basic", True)]


def test_checks_reject_bad_rows(created):
    bad_plan = "INSERT INTO membership (member_name, plan, ends_on, price) VALUES ('X', 'gold', current_date + 1, 1)"
    assert attempt(created, bad_plan) == "23514"
    bad_dates = "INSERT INTO membership (member_name, ends_on, price) VALUES ('X', current_date, 1)"
    assert attempt(created, bad_dates) == "23514"
