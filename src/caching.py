from enum import Enum
import logging
from pathlib import Path
import os
import platform
import pickle

from dataclasses import dataclass

# from ankiAPI.ankiAPI import AnkiAPI
from ankiCard import AnkiCard

logger = logging.getLogger(__name__)

def _get_cache_dir_impl() -> Path:
    """
    Determine the appropriate cache directory based on the operating system.

    # TODO test this

    We check:
    - $XDG_CACHE_HOME (Linux/macOS)
    - ${HOME}/.cache (Linux/macOS fallback)
    - %LOCALAPPDATA% (Windows)
    - /tmp (as a last resort)

    Returns:
        Path: The cache directory.
    """
    if platform.system() == "Windows":
        return Path(os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / "cache"

    # Check Linux/macOS paths
    return Path(
        os.getenv("XDG_CACHE_HOME") or
        (Path(os.getenv("HOME", "/")) / ".cache")
    )

# TODO move this var in main.py or __init__.py
APP_NAME = "ObsidianToAnki"
def get_cache_dir() -> Path:
    sys_cache_dir = _get_cache_dir_impl()
    assert sys_cache_dir != "" and "No cache folder found"

    # TODO this can still be a file and not a dir
    app_cache_dir = sys_cache_dir / APP_NAME
    if not os.path.exists(app_cache_dir):
        os.makedirs(app_cache_dir)

    return app_cache_dir


@dataclass
class LastEditCache:
    """
    #TODO
    We will cache the last time we ran this program
    if file was not edited between last ran of this program and now,
    we don't need to open it
    """
    pass

class Action(Enum):
    CREATE = 0
    UPDATE = 1
    NO_ACTION = 2 # The card is exact match

class AnkiIDCache:
    """
    #TODO handle renames

    We store DeckName -> AnkiNoteID
    To update notes if they changed rather than create new one to avoid duplicates

    We only stone this DeckName -> AnkiNoteID in cache
    the AnkiNoteID -> AnkiCard will need to be populated with .populate()
    Normally it would be one dictionary Deckname -> (AnkiID, AnkiCard),
    but we don't want to store everything as AnkiCard objects can be quite large

    We use lists in caches exclusivly no sets as we will be using these information
    to communicate over http and sets are not json serializable

    Note:
        There can be quite a lot of moving notes around between files
        that target the same deck and it seems impractical to implement it as
        `FilePath -> AnkiNoteID`
        This assumtion acctually might be wrong
    """

    CACHE_FILE = "AnkiIdCache.pkl"
    def __init__(self, anki_api) -> None:
        # self.anki_api: AnkiAPI = anki_api
        self.anki_api = anki_api # Not sure how to solve the circular import
        cache_dir = get_cache_dir()
        cache_file = cache_dir / self.CACHE_FILE
        self._cache: dict[str, list[int]] = self._load_pickle(cache_file)
        self._deck_cache_records: dict[str, set[AnkiCard]] = { }

    def __del__(self) -> None:
        cache_dir = get_cache_dir()
        cache_file = cache_dir / self.CACHE_FILE
        self._save_pickle(cache_file)

    def _load_pickle(self, filename: Path) -> dict[str, list[int]]:
        logger.info(f"Loading from {filename}")
        if not os.path.exists(filename):
            return {}

        with open(filename, 'rb') as file:
            return pickle.load(file)

    def _save_pickle(self, filename: Path) -> None:
        with open(filename, 'wb') as file:
            pickle.dump(self._cache, file, pickle.HIGHEST_PROTOCOL)

    def get(self, deck_name: str, card: AnkiCard) -> Action:
        if deck_name not in self._cache:
            self._cache[deck_name] = []

        if deck_name not in self._deck_cache_records:
            cards = self.anki_api.get_notes_by_id(self._cache[deck_name])
            self._deck_cache_records[deck_name] = \
                { AnkiCard.from_response(body) for body in cards }

        # TODO
        return Action.CREATE
