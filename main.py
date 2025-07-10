from scraper.core.factory import ScraperFactory
from scraper.utils.logger import setup_logger
from scraper.db.postgres_advanced import PostgresAdvancedQueries

def main():
    setup_logger()
    scraper = ScraperFactory.create_scraper("imdb")
    data = scraper.scrape()
    if data:
        scraper.export_to_csv()
        scraper.export_to_db()

        # Ejecutar las consultas SQL avanzadas
        advanced_db = PostgresAdvancedQueries()
        advanced_db.run_advanced_queries()
        advanced_db.close()

if __name__ == "__main__":
    main()
