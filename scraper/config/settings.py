import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.path.join(BASE_DIR, 'data', 'imdb_movies.db')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9"
}


POSTGRES_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "imdb_db",
    "user": "imdb_user",
    "password": "imdb_password"
}