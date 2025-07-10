import psycopg2
from psycopg2 import sql, extras
from scraper.config.settings import POSTGRES_CONFIG
import logging

logger = logging.getLogger(__name__)

class PostgresDB:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=POSTGRES_CONFIG['host'],
                port=POSTGRES_CONFIG['port'],
                database=POSTGRES_CONFIG['database'],
                user=POSTGRES_CONFIG['user'],
                password=POSTGRES_CONFIG['password']
            )
            self.conn.autocommit = False
            logger.info("Conexión a PostgreSQL establecida.")
        except Exception as e:
            logger.error(f"Error conectando a PostgreSQL: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Conexión a PostgreSQL cerrada.")

    def save_movies(self, movies):
        """
        Guarda la lista de películas y sus actores en la base de datos PostgreSQL.
        movies: lista de diccionarios con esta estructura:
            {
                "Título": str,
                "Año": str o int,
                "Calificación": float,
                "Duración (min)": int,
                "Metascore": float o None,
                "Actores principales": "Actor1, Actor2, Actor3"
            }
        """
        try:
            with self.conn.cursor() as cur:
                for movie in movies:
                    # Insertar o actualizar película con ON CONFLICT en (titulo, anio)
                    cur.execute("""
                        INSERT INTO peliculas (titulo, anio, calificacion, duracion, metascore)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (titulo, anio) DO UPDATE
                        SET calificacion = EXCLUDED.calificacion,
                            duracion = EXCLUDED.duracion,
                            metascore = EXCLUDED.metascore
                        RETURNING id;
                    """, (
                        movie.get("Título"),
                        int(movie.get("Año")) if movie.get("Año") else None,
                        movie.get("Calificación"),
                        movie.get("Duración (min)"),
                        movie.get("Metascore")
                    ))
                    pelicula_id = cur.fetchone()[0]

                    # Eliminar actores previos para evitar duplicados
                    cur.execute("DELETE FROM actores WHERE pelicula_id = %s;", (pelicula_id,))

                    # Insertar actores nuevos
                    actores = [a.strip() for a in movie.get("Actores principales", "").split(",")]
                    for actor in actores:
                        if actor:
                            cur.execute("""
                                INSERT INTO actores (pelicula_id, nombre)
                                VALUES (%s, %s);
                            """, (pelicula_id, actor))

                self.conn.commit()
                logger.info("Datos guardados correctamente en PostgreSQL.")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error guardando datos en PostgreSQL: {e}")
            raise
