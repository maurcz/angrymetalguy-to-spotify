import logging
import sys
from typing import Any, Dict, Set

import spotipy
import spotipy.util as util

from angrymetalguy_to_spotify.configuration import (
    SCORE_CUTOFF,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_PLAYLIST_ID,
    SPOTIFY_REDIRECT_URI,
    SPOTIFY_USERNAME,
)


def add_to_playlist(reviews: Dict[str, Any]) -> None:
    """Adds albums to a target spotify playlist. Albums that don't make the cut (via `SCORE_CUTOFF`)
    are skipped.

    Parameters
    ----------
    reviews : Dict[str, Any]
        metadata from scraped reviews
    """
    spotify = _connect()
    albums_in_playlist = _get_albums_in_playlist(spotify)

    for review in reviews:
        if review["score"] < SCORE_CUTOFF:
            continue

        _add_to_playlist(spotify, albums_in_playlist, review["band"], review["album"], review["score"])


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
        logging.error(f"Can't get token for {SPOTIFY_USERNAME}")
        sys.exit()

    return spotipy.Spotify(auth=token)


def _get_albums_in_playlist(spotify: spotipy.Spotify) -> Set[str]:
    """Gets albums currently in the playlist. This is necessary to avoid
    issues down the line with duplicate inserts via the spotipy API.

    Parameters
    ----------
    spotify : spotipy.Spotify
        spotify connection object

    Returns
    -------
    Set[str]
        ids of albums already in the playlist
    """

    all_tracks = []
    offset = 0
    albums = set()

    # There's a limit of 100 tracks per request. This `for` will *always* hit the `break`, unless
    # the playlist has ~~922337203685477580700 tracks
    for _ in range(0, sys.maxsize):
        results = spotify.user_playlist_tracks(
            user=SPOTIFY_USERNAME, playlist_id=SPOTIFY_PLAYLIST_ID, fields="items.track.album.id", offset=offset
        )
        all_tracks.extend(results["items"])
        tracks_retrieved = len(results["items"])
        if tracks_retrieved < 100:
            break
        offset += tracks_retrieved - 1

    # No API to retrieve albums from playlists, just tracks.
    # Simplifying deduping with a set.
    for track in all_tracks:
        albums.add(track["track"]["album"]["id"])

    return albums


def _add_to_playlist(spotify: spotipy.Spotify, albums_in_playlist: Set[str], band: str, album: str, score: float) -> None:
    """Adds a target album to a playlist.

    Tracks are inserted one by one. Once the "album id to be inserted" is retrieved, this function will skip
    if the album is already in the playlist, avoiding insertion errors.

    Parameters
    ----------
    spotify : spotipy.Spotify
        spotify connection object
    albums_in_playlist : Set[str]
        ids of albums alredy in playlist
    band : str
        the band name
    album : str
        the album name
    score : float
        review score. only used for logging purposes.
    """
    results = spotify.search(q="album:" + album + " artist:" + band, limit=1, type="album")

    for item in results["albums"]["items"]:
        # Skips if album already in playlist
        if item["id"] in albums_in_playlist:
            logging.info(f"{band} - {album} ({score}) already in playlist.")
            break

        # No API to add an album by name, must add a group of tracks
        tracks_ids = []
        for track in spotify.album_tracks(item["id"])["items"]:
            tracks_ids.append(track["id"])

        spotify.user_playlist_add_tracks(SPOTIFY_USERNAME, SPOTIFY_PLAYLIST_ID, tracks_ids)

        logging.info(f"{band} - {album} ({score}) added to playlist.")
