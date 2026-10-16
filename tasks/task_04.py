def create_script() -> str:
    return """
CREATE TABLE membership (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    member_name varchar(100) NOT NULL,
    email varchar(120) UNIQUE,
    plan varchar(10) NOT NULL DEFAULT 'basic' CHECK (plan IN ('basic', 'pro', 'vip')),
    started_on date NOT NULL DEFAULT CURRENT_DATE,
    ends_on date NOT NULL,
    price numeric(8, 2) NOT NULL CHECK (price >= 0),
    CONSTRAINT chk_membership_dates CHECK (ends_on > started_on)
);
""".strip()