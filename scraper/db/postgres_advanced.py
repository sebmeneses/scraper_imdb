import logging
from psycopg2 import connect, sql
from scraper.config.settings import POSTGRES_CONFIG

logger = logging.getLogger(__name__)

class PostgresAdvancedQueries:
    def __init__(self):
        try:
            self.conn = connect(
                host=POSTGRES_CONFIG['host'],
                port=POSTGRES_CONFIG['port'],
                database=POSTGRES_CONFIG['database'],
                user=POSTGRES_CONFIG['user'],
                password=POSTGRES_CONFIG['password']
            )
            self.conn.autocommit = True
            logger.info("Conexión a PostgreSQL para consultas avanzadas establecida.")
        except Exception as e:
            logger.error(f"Error conectando a PostgreSQL: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Conexión a PostgreSQL cerrada.")

    def run_advanced_queries(self):
        with self.conn.cursor() as cur:
            # Leer el SQL de archivo
            with open("scraper/db/advanced_queries.sql", "r", encoding="utf-8") as f:
                sql_commands = f.read()
            try:
                cur.execute(sql_commands)
                # Si quieres recuperar resultados de las consultas, deberías separarlas y hacer fetch aquí.
                logger.info("Consultas avanzadas ejecutadas correctamente.")
            except Exception as e:
                logger.error(f"Error ejecutando consultas avanzadas: {e}")
                raise
