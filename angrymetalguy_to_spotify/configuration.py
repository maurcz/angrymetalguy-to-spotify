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
SPOTIFY_PLAYLIST_05_ID = os.environ["SPOTIFY_PLAYLIST_05_ID"]
SPOTIFY_PLAYLIST_10_ID = os.environ["SPOTIFY_PLAYLIST_10_ID"]
SPOTIFY_PLAYLIST_15_ID = os.environ["SPOTIFY_PLAYLIST_15_ID"]
SPOTIFY_PLAYLIST_20_ID = os.environ["SPOTIFY_PLAYLIST_20_ID"]
SPOTIFY_PLAYLIST_25_ID = os.environ["SPOTIFY_PLAYLIST_25_ID"]
SPOTIFY_PLAYLIST_30_ID = os.environ["SPOTIFY_PLAYLIST_30_ID"]
SPOTIFY_PLAYLIST_35_ID = os.environ["SPOTIFY_PLAYLIST_35_ID"]
SPOTIFY_PLAYLIST_40_ID = os.environ["SPOTIFY_PLAYLIST_40_ID"]
SPOTIFY_PLAYLIST_45_ID = os.environ["SPOTIFY_PLAYLIST_45_ID"]
SPOTIFY_PLAYLIST_50_ID = os.environ["SPOTIFY_PLAYLIST_50_ID"]
SPOTIFY_PLAYLIST_ROTATION_ID = os.environ["SPOTIFY_PLAYLIST_ROTATION_ID"]

# Number of pages to scan for reviews
NUMBER_OF_PAGES = int(os.environ["NUMBER_OF_PAGES"])

# Errors can be useful for local debugging, but we must skip any issues when
# running inside the lambda. If this is `True`, skips Exceptions during scraping
SUPRESS_SCRAPING_ERRORS = bool(os.environ["SUPRESS_SCRAPING_ERRORS"])
