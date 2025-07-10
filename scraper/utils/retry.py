import requests
import time
import logging

TOR_PROXIES = {
    'http': 'socks5h://127.0.0.1:9150',
    'https': 'socks5h://127.0.0.1:9150'
}


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def retry_request(url, headers, retries=3, backoff=2):
    for attempt in range(retries):
        try:
            # Verificar IP actual
            ip_response = requests.get("http://httpbin.org/ip", proxies=TOR_PROXIES, timeout=10)
            logger.info(f"[Intento {attempt+1}] IP actual de Tor: {ip_response.text.strip()}")

            # Hacer request
            response = requests.get(url, headers=headers, proxies=TOR_PROXIES, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            logger.warning(f"Request error on {url}: {e} (intento {attempt+1}/{retries})")
            if attempt == retries - 1:
                logger.error(f"Max retries reached for {url}")
                raise
            sleep = backoff ** attempt
            logger.info(f"⏳ Reintentando en {sleep} segundos...")
            time.sleep(sleep)
