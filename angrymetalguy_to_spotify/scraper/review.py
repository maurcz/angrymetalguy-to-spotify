import re
import unicodedata
from collections import defaultdict
from typing import Dict, List, Tuple

from bs4.element import Tag

from angrymetalguy_to_spotify.configuration import SUPRESS_SCRAPING_ERRORS
from angrymetalguy_to_spotify.constants import RATING_SYSTEM, UNKNOWN_SCORE_VALUE
from angrymetalguy_to_spotify.scraper.utils import soup
from angrymetalguy_to_spotify.utils.logger import get_logger

logger = get_logger()


class ScoreParsingError(Exception):
    pass


def scrape_reviews(urls: List[str]) -> Dict[float, List[Dict[str, str]]]:
    """Scrape posts for album review scores. The process will try to parse
    band/albums/scores from all urls, ignoring errors.

    Parameters
    ----------
    urls : List[str]
        target urls

    Returns
    -------
    Dict[float, List[Dict[str, str]]
        list of reviews metadata
    """
    result = defaultdict(list)

    for url in urls:
        post = soup(url)
        band, album = _parse_title(post.find("h1", class_="entry-title"))
        score = _parse_score(post.find("div", class_="entry-content"))

        # Deliberately skip albums that couldn't be scored due to parsing errors.
        # Posts that are not reviews will fall into this condition.
        if score == UNKNOWN_SCORE_VALUE:
            continue

        result[score].append({"band": band, "album": album})

    return result


def _parse_title(entry_title: Tag) -> Tuple[str, str]:
    """Tries to get the Band and Album name from the post title.

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
        # Getting rid of the word "review"
        pattern = re.compile(" [Rr]eview$")
        title = pattern.sub("", entry_title.text)

        # Album titles might contain dashes, only the first one can be used for the split
        idx = title.find(" – ")
        band = title[:idx]
        album = title[idx + 3 :]  # noqa

        return band, album

    except Exception as ex:
        if not SUPRESS_SCRAPING_ERRORS:
            logger.exception(ex)
        # Some posts are not reviews; returning empty as a signal for this to be
        # ignored when adding to spotify
        return "", ""


def _parse_score(entry_content: Tag) -> str:
    """Tries to parse the score from a review post.

    Note that reviews can be floats or text; refer to constant `RATING_SYSTEM` for
    a better explanation.

    Parameters
    ----------
    entry_content : Tag
        soup object representing the contents of a post

    Returns
    -------
    str
        review score
    """
    # Some posts have annoying characters, normalizing. Also replacing weird line breaks.
    text = unicodedata.normalize("NFKD", entry_content.text).replace("↩", "\n")

    # Ratings are generally at the bottom of the review post, with formats like:
    # - Rating: X.X
    # - Rating: Great
    # This pattern matches "Rating: " + either words or numbers with decimal points
    rating = re.search("Rating:\s*([\w.]+)", text)  # noqa

    try:
        score = rating.group(1).strip()

        # First check if it's a simple float (pattern will match values like '1.5', '4.0', etc)
        if bool(re.match(r"^\d+\.\d+$", score)):
            return score

        # Check if a word was used for scoring
        if score in RATING_SYSTEM:
            return RATING_SYSTEM[score]

        # Check again if it's a word, but filter anything that's not letters
        cleaned_score = re.sub("[^a-zA-Z]", "", score)
        if cleaned_score in RATING_SYSTEM:
            return RATING_SYSTEM[cleaned_score]

        # 残念 ¯\_(ツ)_/¯
        raise ScoreParsingError(f"Can't parse value '{score}'.")

    except Exception as ex:
        # Errors can be useful for local debugging, but we must skip any issues when
        # running inside in AWS Lamba
        if not SUPRESS_SCRAPING_ERRORS:
            logger.exception(ex)

        # If any issues occur during parsing, just mark the score as "unknown"
        return UNKNOWN_SCORE_VALUE
