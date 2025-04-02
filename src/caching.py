from pathlib import Path
import os
import platform
import pickle

from dataclasses import dataclass

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

class AnkiIDsCache:
    """
    #TODO handle renames

    We store DeckName -> AnkiNoteID
    To update notes if they changed rather than create new one to avoid duplicates

    Note:
        There can be quite a lot of moving notes around between files
        that target the same deck and it seems impractical to implement it as
        `FilePath -> AnkiNoteID`
        This assumtion acctually might be wrong
    """

    CACHE_FILE = "AnkiIdCache.pkl"
    def __init__(self) -> None:
        cache_dir = get_cache_dir()
        cache_file = cache_dir / self.CACHE_FILE
        self._cache = self._load_pickle(cache_file)

    def _load_pickle(self, filename: Path) -> dict[str, int]:
        if not os.path.exists(filename):
            return {}

        with open(filename, 'rb') as file:
             return pickle.load(file)

    def __getitem__(self, deckname: str) -> int:
        return self._cache[deckname]

    def get(self, deckname: str) -> int | None:
        return self._cache.get(deckname)
