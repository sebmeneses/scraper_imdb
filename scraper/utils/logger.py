import logging
import os

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", "scraper.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
