from typing import List

from .constants import BASE_URL
from .utils import soup


def get_posts_links(number_of_pages: int) -> List[str]:
    """Gets all posts links from X pages.

    Parameters
    ----------
    number_of_pages : int
        number of pages to scrape for links

    Returns
    -------
    List[str]
        list of links for posts
    """
    posts = []

    for i in range(1, number_of_pages + 1):
        url = f"{BASE_URL}" if i == 1 else f"{BASE_URL}page/{i}"
        posts.extend(_get_posts_from_page(url))

    return posts


def _get_posts_from_page(url: str) -> List[str]:
    """Gets all posts links from a single page

    Parameters
    ----------
    url : str
        target url

    Returns
    -------
    List[str]
        list of links for posts
    """
    titles = soup(url).find_all("h2", class_="entry-title")
    return [a.find("a").get("href") for a in titles]
