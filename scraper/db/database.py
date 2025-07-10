import os
import sqlite3
import pandas as pd
import logging
from scraper.config.settings import DB_PATH

logger = logging.getLogger(__name__)

def save_movies_to_db(data_list):
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        df = pd.DataFrame(data_list)
        df.to_sql('movies', conn, if_exists='replace', index=False)
        conn.close()
        logger.info(f"Datos guardados en BD SQLite: {DB_PATH}")
    except Exception as e:
        logger.error(f"Error guardando en BD: {e}")
