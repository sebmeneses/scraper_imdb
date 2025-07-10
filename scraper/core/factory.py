from scraper.core.imdb_scraper import IMDBScraper

class ScraperFactory:
    @staticmethod
    def create_scraper(source):
        if source == "imdb":
            return IMDBScraper()
        else:
            raise ValueError(f"Scraper para fuente '{source}' no implementado.")
