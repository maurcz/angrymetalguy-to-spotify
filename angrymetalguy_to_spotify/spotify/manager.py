import sys
from datetime import datetime, timedelta
from typing import Dict, List, Set

import spotipy

from angrymetalguy_to_spotify.configuration import SPOTIFY_USERNAME
from angrymetalguy_to_spotify.constants import DAYS_CUTOFF
from angrymetalguy_to_spotify.utils.logger import get_logger

logger = get_logger()


class PlaylistManager:
    """Interacts with Spotify Playlists"""

    def __init__(self, spotify: spotipy.Spotify, playlist_id: str, old_albums_limit_in_days: int = 0):
        self._spotify = spotify
        self._playlist_id = playlist_id
        self._user = SPOTIFY_USERNAME
        self._old_albums_limit_in_days = old_albums_limit_in_days  # 0 means no limits, no albums are cleaned up
        self._albums_in_playlist, self._old_tracks_in_playlist = self._get_albums_in_playlist()

    def add_to_playlist(self, albums: List[Dict[str, str]]) -> None:
        """Adds albums to a playlist.

        Tracks are inserted one by one. Once the "album id to be inserted" is retrieved, this function will skip
        if the album is already in the playlist, avoiding insertion errors.

        Parameters
        ----------
        albums: List[Dict[str, str]]
            List of all albums to be added to the playlist
        """
        logger.info(f"Adding albums to playlist {self._playlist_id}...")

        for album in albums:
            results = self._spotify.search(q="album:" + album["album"] + " artist:" + album["band"], limit=1, type="album")

            for item in results["albums"]["items"]:
                # Skips if album already in playlist
                if item["id"] in self._albums_in_playlist:
                    logger.info(f"{album['album']} - {album['band']} already in playlist.")
                    break

                # No API to add an album by name, must add a group of tracks
                tracks_ids = []
                for track in self._spotify.album_tracks(item["id"])["items"]:
                    tracks_ids.append(track["id"])

                self._spotify.user_playlist_add_tracks(SPOTIFY_USERNAME, self._playlist_id, tracks_ids)

                logger.info(f"{album['album']} - {album['band']} added to playlist.")

    def remove_old_tracks(self) -> None:
        """
        Removes all tracks that have been sitting on the playlist for more than `self._old_albums_limit_in_days`
        """
        self._spotify.user_playlist_remove_all_occurrences_of_tracks(self._user, self._playlist_id, self._old_tracks_in_playlist)
        logger.info(f"Removed tracks older than {self._old_albums_limit_in_days} days from playlist {self._playlist_id}")

    def _get_albums_in_playlist(self) -> Set[str]:
        """Gets albums currently in the playlist. This is necessary to avoid
        issues down the line with duplicate inserts via the spotipy API.

        Returns
        -------
        Tuple(Set[str], Set[str])
            Set[str] - ids of albums already in the playlist
            Set[str] - ids of tracks that have been in the playslit for longer than `self._old_albums_limit_in_days`
        """

        all_tracks = []
        offset = 0
        unique_albums = set()
        old_tracks = []

        # There's a limit of 100 tracks per request. This `for` will *always* hit the `break`, unless
        # the playlist has ~~922337203685477580700 tracks
        for _ in range(0, sys.maxsize):
            results = self._spotify.user_playlist_tracks(
                user=self._user,
                playlist_id=self._playlist_id,
                fields="items.track.album.id,items.track.id,items.added_at",
                offset=offset,
            )
            all_tracks.extend(results["items"])
            tracks_retrieved = len(results["items"])
            if tracks_retrieved < 100:
                break
            offset += tracks_retrieved - 1

        for track in all_tracks:
            # No API to retrieve albums from playlists, just tracks.
            # Simplifying deduping with a set.
            unique_albums.add(track["track"]["album"]["id"])

            # 0 means no albums should be considered for cleanup
            if self._old_albums_limit_in_days == 0:
                continue

            # Marking albums that have been in the playlist for a while
            added_at = datetime.strptime(track["added_at"], "%Y-%m-%dT%H:%M:%SZ")
            date_cutoff = datetime.utcnow() - timedelta(days=DAYS_CUTOFF)

            if added_at < date_cutoff:
                old_tracks.append(track["track"]["id"])

        return unique_albums, old_tracks
