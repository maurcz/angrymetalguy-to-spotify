import logging
import time

import requests
from bs4 import BeautifulSoup

from .constants import GLOBAL_DELAY


def soup(url: str) -> BeautifulSoup:
    time.sleep(GLOBAL_DELAY)
    logging.info(f"Scraping {url}")
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")
