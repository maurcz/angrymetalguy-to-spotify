import time

import requests
from bs4 import BeautifulSoup

from angrymetalguy_to_spotify.constants import GLOBAL_DELAY
from angrymetalguy_to_spotify.utils.logger import get_logger

logger = get_logger()


def soup(url: str) -> BeautifulSoup:
    time.sleep(GLOBAL_DELAY)
    logger.info(f"Scraping {url}")
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")
