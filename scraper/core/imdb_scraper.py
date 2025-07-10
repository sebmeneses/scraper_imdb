import json
import time
import logging
import os
from bs4 import BeautifulSoup
from scraper.utils.retry import retry_request
from scraper.utils.tools import iso8601_to_minutes
from scraper.config.settings import HEADERS
from scraper.db.postgres_db import PostgresDB

logger = logging.getLogger(__name__)

class IMDBScraper:
    def __init__(self, top_n=50):
        self.url = "https://www.imdb.com/chart/top/"
        self.top_n = top_n
        self.data_list = []

    def scrape(self):
        try:
            response = retry_request(self.url, headers=HEADERS)
            soup = BeautifulSoup(response.text, "html.parser")
            script_tag = soup.find("script", type="application/ld+json")
            if not script_tag:
                logger.error("No se encontró el bloque <script type='application/ld+json'>.")
                return []

            data = json.loads(script_tag.string)
            movies = data.get("itemListElement", [])

            for idx, movie_entry in enumerate(movies[:self.top_n], start=1):
                movie = movie_entry["item"]
                title = movie.get("name")
                rating = movie.get("aggregateRating", {}).get("ratingValue")
                duration_iso = movie.get("duration", "")
                duration_min = iso8601_to_minutes(duration_iso)
                url = movie.get("url")
                year = movie.get("datePublished", "")[:4]

                # Detalles
                time.sleep(1)
                try:
                    res_detail = retry_request(url, headers=HEADERS)
                    soup_detail = BeautifulSoup(res_detail.text, "html.parser")

                    # Actores
                    actor_tags = soup_detail.select('a[data-testid="title-cast-item__actor"]')[:3]
                    actors = [a.text.strip() for a in actor_tags]

                    # Año si no vino en JSON
                    if not year:
                        header_tag = soup_detail.select_one('ul.ipc-inline-list li a[href*="/releaseinfo"]')
                        if header_tag:
                            year = header_tag.text.strip()

                    # Extraer Metascore por clase CSS
                    metascore_span = soup_detail.select_one('span.sc-9fe7b0ef-0.hDuMnh.metacritic-score-box')
                    if metascore_span:
                        try:
                            metascore = int(metascore_span.text.strip())
                        except ValueError:
                            metascore = None
                    else:
                        metascore = None

                except Exception as e:
                    logger.error(f"Error al obtener detalles de {title}: {e}")
                    actors = []
                    metascore = None
                    if not year:
                        year = ""

                logger.info(f"{idx}. {title} ({year}) | {rating} | {duration_min} min | Metascore: {metascore}")
                logger.info(f"    Actores principales: {', '.join(actors)}")

                self.data_list.append({
                    "Título": title,
                    "Año": year,
                    "Calificación": rating,
                    "Duración (min)": duration_min,
                    "Metascore": metascore,
                    "Actores principales": ", ".join(actors)
                })

            return self.data_list

        except Exception as e:
            logger.error(f"Error en scrapeo principal: {e}")
            return []

    def export_to_csv(self, filename="data/imdb_top_50.csv"):
        import pandas as pd
        if not self.data_list:
            logger.warning("No hay datos para exportar a CSV.")
            return
        abs_path = os.path.abspath(filename)
        logger.info(f"Intentando guardar CSV en: {abs_path}")
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)

        df = pd.DataFrame(self.data_list)
        df.to_csv(abs_path, index=False, encoding="utf-8")
        logger.info(f"CSV guardado: {abs_path}")

    def export_to_db(self):
        if not self.data_list:
            logger.warning("No hay datos para exportar a BD.")
            return
        db = PostgresDB()
        db.save_movies(self.data_list)
