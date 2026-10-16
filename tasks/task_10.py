def migration_script() -> str:
    return """
BEGIN;

-- 1. Створення таблиці-довідника city
CREATE TABLE city (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(60) NOT NULL UNIQUE
);

-- 2. Перенесення унікальних непорожніх міст без зайвих пропусків
INSERT INTO city (name)
SELECT DISTINCT btrim(city)
FROM client
WHERE city IS NOT NULL AND btrim(city) <> '';

-- 3. Додавання зовнішнього ключа та заповнення посилань
ALTER TABLE client
    ADD COLUMN city_id integer REFERENCES city(id) ON DELETE SET NULL;

UPDATE client c
SET city_id = ci.id
FROM city ci
WHERE btrim(c.city) = ci.name;

-- 4. Видалення старого стовпця
ALTER TABLE client
    DROP COLUMN city;

-- 5. Обмеження унікальності номерів телефонів
ALTER TABLE client
    ADD CONSTRAINT uq_client_phone UNIQUE (phone);

-- 6. Оновлення поточної версії схеми
INSERT INTO schema_version (version, description)
VALUES (2, 'city dictionary');

COMMIT;
""".strip()