import sys
from typing import Dict, List

import spotipy
import spotipy.util as util

from angrymetalguy_to_spotify.configuration import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_PLAYLIST_05_ID,
    SPOTIFY_PLAYLIST_10_ID,
    SPOTIFY_PLAYLIST_15_ID,
    SPOTIFY_PLAYLIST_20_ID,
    SPOTIFY_PLAYLIST_25_ID,
    SPOTIFY_PLAYLIST_30_ID,
    SPOTIFY_PLAYLIST_35_ID,
    SPOTIFY_PLAYLIST_40_ID,
    SPOTIFY_PLAYLIST_45_ID,
    SPOTIFY_PLAYLIST_50_ID,
    SPOTIFY_PLAYLIST_ROTATION_ID,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_USERNAME,
)
from angrymetalguy_to_spotify.constants import SCORE_CUTOFF
from angrymetalguy_to_spotify.spotify.manager import PlaylistManager
from angrymetalguy_to_spotify.utils.logger import get_logger

logger = get_logger()


def add_to_playlist(reviews: Dict[float, List[Dict[str, str]]]) -> None:
    """Adds albums to a target spotify playlist.

    Parameters
    ----------
    reviews : Dict[float, List[Dict[str, str]]]
        metadata from scraped reviews, categorized by score
    """

    spotify = _connect()

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_05_ID, old_tracks_limit_in_days=365)
    manager.add_to_playlist(reviews["0.5"])

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_10_ID, old_tracks_limit_in_days=365)
    manager.add_to_playlist(reviews["1.0"])

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_10_ID, old_tracks_limit_in_days=365)
    manager.add_to_playlist(reviews["1.0"])

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_15_ID, old_tracks_limit_in_days=365)
    manager.add_to_playlist(reviews["1.5"])

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_20_ID, old_tracks_limit_in_days=365)
    manager.add_to_playlist(reviews["2.0"])

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_25_ID, old_tracks_limit_in_days=365)
    manager.add_to_playlist(reviews["2.5"])

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_30_ID, old_tracks_limit_in_days=365)
    manager.add_to_playlist(reviews["3.0"])

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_35_ID, old_tracks_limit_in_days=365)
    manager.add_to_playlist(reviews["3.5"])

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_40_ID, old_tracks_limit_in_days=365)
    manager.add_to_playlist(reviews["4.0"])

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_45_ID, old_tracks_limit_in_days=365)
    manager.add_to_playlist(reviews["4.5"])

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_50_ID, old_tracks_limit_in_days=365)
    manager.add_to_playlist(reviews["5.0"])

    manager = PlaylistManager(spotify, SPOTIFY_PLAYLIST_ROTATION_ID, old_tracks_limit_in_days=60)
    manager.add_to_playlist(_filter_by_score(reviews=reviews, score_cutoff=SCORE_CUTOFF))
    manager.remove_old_tracks()


def _connect() -> spotipy.Spotify:
    """Opens up a spotify connection. This process is completely dictated by `spotipy`, so refer to
    README.md for a complete explanation of the flow.

    The access scope of the token is decreased as much as possible.

    Returns
    -------
    spotipy.Spotify
        _description_
    """
    scope = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative"

    token = util.prompt_for_user_token(
        username=SPOTIFY_USERNAME,
        scope=scope,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
    )

    if token is None:
        logger.error(f"Can't get token for {SPOTIFY_USERNAME}")
        sys.exit()

    return spotipy.Spotify(auth=token)


def _filter_by_score(reviews: Dict[float, List[Dict[str, str]]], score_cutoff: int) -> List[Dict[str, str]]:
    """Filters reviews based on a `score_cutoff`. Only scores that are greater than the cutoff will
    be present in the returning list.

    Parameters
    ----------
    reviews : Dict[float, List[Dict[str, str]]]
        reviews to filter
    score_cutoff : int
        target score cutoff

    Returns
    -------
    List[Dict[str, str]]
        filtered list
    """
    # Prepping data for "special" playlists
    filtered = []
    for key, value in reviews.items():
        try:
            converted = float(key)
        except Exception:
            logger.warning(f"Key {key} cannot be converted to float. Ignoring...")
            continue

        if converted >= score_cutoff:
            filtered += value

    return filtered
