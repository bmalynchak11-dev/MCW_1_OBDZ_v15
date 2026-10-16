# Стартовий проєкт

1. Відкрийте проєкт у GitHub Codespaces (Code → Codespaces → Create codespace): devcontainer сам запустить Python і PostgreSQL 18. Локально: запустіть `docker run -d --name obdz-pg -e POSTGRES_PASSWORD=postgres -p 127.0.0.1:5432:5432 postgres:18`, потім `python -m venv .venv`, активація, `pip install -r requirements.txt`.
2. Знайдіть свої файли в папці `tasks/` і реалізуйте їх за картками.
3. Запускайте відкриті тести: `pytest` або `pytest tests/test_task_NN.py`.
4. Змінюйте лише свої файли в `tasks/` (і за бажанням `tests/test_my.py`).
5. Завдання 4, 8 і 10 потребують PostgreSQL: перевірте змінні `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD` (у Codespaces їх уже задано).
6. Теоретичні завдання 11–15 не мають тестів: умова й місце для відповіді є у файлах `answers/task_11.md` … `answers/task_15.md`. Напишіть відповідь після рядка «Відповідь:» і здайте файли вибраних завдань.
