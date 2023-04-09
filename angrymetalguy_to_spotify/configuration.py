import os

from dotenv import load_dotenv

load_dotenv()

"""Use `make .env` to populate a local file with all the env var names."""

# Spotify OAuth
SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_USERNAME = os.environ["SPOTIFY_USERNAME"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]

# Playlist that will get the albums
SPOTIFY_PLAYLIST_ID = os.environ["SPOTIFY_PLAYLIST_ID"]

# Only scores above this number will be added to the playlist
SCORE_CUTOFF = float(os.environ["SCORE_CUTOFF"])

# Number of pages to scan for reviews
NUMBER_OF_PAGES = int(os.environ["NUMBER_OF_PAGES"])

# Scraping will always ignore parsing errors, but those can be useful for debugging.
# However, if deploying this to aws lambda you have to skip `logging.exception`
SUPRESS_SCRAPING_ERRORS = bool(os.environ["SUPRESS_SCRAPING_ERRORS"])
