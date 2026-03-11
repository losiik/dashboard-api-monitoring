import os
from dotenv import load_dotenv

if os.path.exists('.env'):
    load_dotenv('.env')

from yoyo import get_backend, read_migrations

from app.settings import settings
from app.scheduler import start_scheduler


def main():
    backend = get_backend(settings.sql_alchemy_connection_url.replace("+psycopg2", ""))
    migrations = read_migrations('./migrations')

    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

    start_scheduler()


if __name__ == "__main__":
    main()
