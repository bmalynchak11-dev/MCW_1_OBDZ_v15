"""Відкриті приклади 10 (з картки). Повний набір перевірок — у викладача."""
from conftest import load
from pgutil import columns, constraints

M = load(10)

SETUP = """
CREATE TABLE client (id integer PRIMARY KEY, name varchar(100) NOT NULL, city varchar(60), phone varchar(20));
CREATE TABLE schema_version (version integer PRIMARY KEY, description varchar(100) NOT NULL,
                             applied_at timestamptz NOT NULL DEFAULT now());
INSERT INTO schema_version (version, description) VALUES (1, 'client table');
INSERT INTO client VALUES (1, 'Іваненко', ' Kyiv ', '050'), (2, 'Петренко', 'Lviv', NULL),
                          (3, 'Сидоренко', '   ', NULL), (4, 'Коваль', NULL, '067'), (5, 'Мельник', 'Kyiv', '093');
"""


def migrate(db):
    db.run(SETUP)
    sql = M.migration_script()
    assert isinstance(sql, str), "migration_script() має повертати рядок з SQL"
    db.run(sql)


def test_card_example_data(db):
    migrate(db)
    assert db.rows("SELECT name FROM city ORDER BY name") == [("Kyiv",), ("Lviv",)]
    assert db.rows("SELECT c.id, y.name FROM client c LEFT JOIN city y ON y.id = c.city_id ORDER BY c.id") == [
        (1, "Kyiv"), (2, "Lviv"), (3, None), (4, None), (5, "Kyiv")]


def test_card_example_structure(db):
    migrate(db)
    assert "city" not in columns(db, "client")
    assert columns(db, "client")["city_id"]["type"] == "integer"
    fks = [c for c in constraints(db, "client") if c["type"] == "f"]
    assert [(c["cols"], c["ref"], c["on_delete"]) for c in fks] == [(["city_id"], "city", "n")]
    assert db.rows("SELECT version, description FROM schema_version ORDER BY version") == [
        (1, "client table"), (2, "city dictionary")]
