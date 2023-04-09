import logging

from angrymetalguy_to_spotify.configuration import NUMBER_OF_PAGES
from angrymetalguy_to_spotify.scraper.links import get_posts_links
from angrymetalguy_to_spotify.scraper.review import scrape_reviews
from angrymetalguy_to_spotify.spotify.playlist import add_to_playlist

logging.basicConfig(level=logging.INFO)


def lambda_start(event, context):
    """Entrypoint for AWS Lambda"""
    start()


def run():
    """Local entrypoint"""
    start()


def start():
    # Get all post links from pages
    urls = get_posts_links(NUMBER_OF_PAGES)

    # Scrape reviews out of each post
    reviews = scrape_reviews(urls)

    # Add scraped albums from reviews to playlist
    add_to_playlist(reviews)


if __name__ == "__main__":
    run()
