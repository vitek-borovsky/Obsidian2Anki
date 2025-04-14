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
        # this should be redundant
        _backup = self._cache

        # remove duplicattes
        self._cache = \
            { key: list(set(val)) for key, val in self._cache.items() }

        if _backup != self._cache:
            logger.warning("Cache was trimmed")

        logger.info(f"Saving to {filename} data:{self._cache}")
        with open(filename, 'wb') as file:
            pickle.dump(self._cache, file, pickle.HIGHEST_PROTOCOL)

    def get(self, card: AnkiCard) -> tuple[Action, int]:
        logger.debug(f"Processing {card.__repr__()}")
        if card.deck_name not in self._cache:
            self._cache[card.deck_name] = []

        if card.deck_name not in self._deck_cache_records:
            logger.info(f"{card.deck_name} not fond in self._deck_cache_records, populating...")
            cards = self.anki_api.get_notes_by_id(self._cache[card.deck_name])

            self._deck_cache_records[card.deck_name] = set()
            for body in cards:
                res = AnkiCard.from_response(body)
                if res is None:
                    continue
                self._deck_cache_records[card.deck_name].add(res)

        cache_records = self._deck_cache_records[card.deck_name]
        logger.debug(f"cache_records[{card.deck_name}]: {cache_records}")

        for i_card in cache_records:
            if card == i_card:
                logger.debug("Card found, no action needed")
                return Action.NO_ACTION, 0 # card exists in exact form

            if card.is_almost_same(i_card):
                logger.debug("Card found, update needed")
                return Action.UPDATE, i_card.id

        logger.debug("Card not found, creating...")
        return Action.CREATE, 0 # New card

    def cache(self, deck_name: str, id: int) -> None:
        if deck_name not in self._cache:
            self._cache[deck_name] = []

        self._cache[deck_name].append(id)
