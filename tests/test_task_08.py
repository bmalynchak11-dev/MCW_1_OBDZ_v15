"""Відкриті приклади 08 (з картки). Повний набір перевірок — у викладача."""
from datetime import date

from conftest import load

M = load(8)

SETUP = """
CREATE TABLE stock (sku varchar(20) PRIMARY KEY, qty integer NOT NULL CHECK (qty >= 0), last_delivery date);
CREATE TABLE delivery (id integer PRIMARY KEY, sku varchar(20) NOT NULL, qty integer NOT NULL, delivered_on date NOT NULL);
CREATE TABLE stock_log (id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY, sku varchar(20) NOT NULL,
                        action varchar(6) NOT NULL CHECK (action IN ('insert', 'update')), qty_after integer NOT NULL);
INSERT INTO stock VALUES ('PEN', 10, '2000-01-10'), ('INK', 4, NULL);
INSERT INTO delivery VALUES (1, 'PEN', 5, '2000-02-01'), (2, 'PEN', 3, '2000-02-15'), (3, 'PEN', -2, '2000-03-01'),
                            (4, 'BAG', 7, '2000-02-05'), (5, 'INK', 0, '2000-02-06');
"""


def test_card_example(db):
    db.run(SETUP)
    sql = M.receive_script()
    assert isinstance(sql, str), "receive_script() має повертати рядок з SQL"
    db.run(sql)
    assert db.rows("SELECT sku, qty, last_delivery FROM stock ORDER BY sku") == [
        ("BAG", 7, date(2000, 2, 5)), ("INK", 4, None), ("PEN", 18, date(2000, 2, 15))]
    assert db.rows("SELECT sku, action, qty_after FROM stock_log ORDER BY sku") == [
        ("BAG", "insert", 7), ("PEN", "update", 18)]


def test_deliveries_are_not_changed(db):
    db.run(SETUP)
    db.run(M.receive_script())
    assert db.value("SELECT count(*) FROM delivery") == 5
