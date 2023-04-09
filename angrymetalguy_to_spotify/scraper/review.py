import logging
import re
import unicodedata
from typing import Any, Dict, List, Tuple

from bs4.element import Tag

from angrymetalguy_to_spotify.configuration import SUPRESS_SCRAPING_ERRORS

from .constants import RATING_SYSTEM
from .utils import soup


def scrape_reviews(urls: List[str]) -> List[Dict[str, Any]]:
    """Scrape posts for album reviews. The process will ignore parsing errors
    and try to parse band/albums/scores from all urls.

    Parameters
    ----------
    urls : List[str]
        target urls

    Returns
    -------
    List[Dict[str, Any]]
        list of reviews metadata
    """
    result = []

    for url in urls:
        post = soup(url)
        band, album = _parse_title(post.find("h1", class_="entry-title"))

        result.append({"band": band, "album": album, "score": _parse_score(post.find("div", class_="entry-content"))})

    return result


def _parse_title(entry_title: Tag) -> Tuple[str, str]:
    """Tries to get an the Band and Album name from the post title.

    Parameters
    ----------
    entry_title : Tag
        soup object representing a h1 title

    Returns
    -------
    Tuple[str, str]
        (Band, Album)
    """
    try:
        # Getting rid of the word review
        pattern = re.compile(" [Rr]eview$")
        title = pattern.sub("", entry_title.text)

        # Album titles might contain dashes, only the first one can be used for the split
        idx = title.find(" – ")
        band = title[:idx]
        album = title[idx + 3 :]  # noqa

        return band, album

    except Exception as ex:
        # Some posts are not reviews; returning empty as a signal for this to be
        # ignored when adding to spotify
        if not SUPRESS_SCRAPING_ERRORS:
            logging.exception(ex)
        return "", ""


def _parse_score(entry_content: Tag) -> float:
    """Tries to parse the score from a review post.

    Note that reviews can be floats or text; rever to constant `RATING_SYSTEM` for
    a better explanation.

    Parameters
    ----------
    entry_content : Tag
        soup object representing the contents of a post

    Returns
    -------
    float
        review score
    """
    # Some posts have annoying characters, normalizing. Also replacing weird line breaks.
    text = unicodedata.normalize("NFKD", entry_content.text).replace("↩", "\n")

    # Rating are generally at the bottom of the review post, with formats like:
    # - Rating: X.X
    # - Raging: Great
    # So this matches "Rating: " + either words or numbers with decimal points
    rating = re.search("Rating:\s*([\w.]+)", text)  # noqa

    try:
        score = rating.group(1).strip()
        return float(score) if score not in RATING_SYSTEM else RATING_SYSTEM[score]
    except Exception as ex:
        # Some posts won't have ratings so we score them as 0.0
        # This ensures it gets skipped according to the cutoff when adding to spotify
        if not SUPRESS_SCRAPING_ERRORS:
            logging.exception(ex)
        return 0.0
