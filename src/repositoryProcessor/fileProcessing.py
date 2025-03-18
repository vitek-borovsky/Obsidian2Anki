from typing import IO

from .fileProcessingConstants import *
from ankiCard import AnkiFileRecord
from .magicChecker import MagicChecker, ObsidianMagicChecker


class File:
    """Represent open file in memory
    File is proccessed as followed
    - Metadata is read and checked for magic,
      if no magic is present we exit
    - Read and store target deck name
    - Process the rest of the file and create AnkiCard objects
    """
    # TODO
    def __init__(self, readable: IO[str]) -> None:
        self.readable = readable
        self.magic_checker: MagicChecker = ObsidianMagicChecker()

    def process_file(self) -> AnkiFileRecord:
        magic = self.magic_checker.get_magic(self.readable)
        if magic is None:
            return AnkiFileRecord("NONE")

        raise NotImplemented
