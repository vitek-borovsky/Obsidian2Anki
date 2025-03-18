from typing import IO, Generator
import re

from .fileProcessingConstants import FileProcessingConstans
from ..ankiCard import AnkiBasicCard, AnkiCard, AnkiFileRecord, get_empty_anki_generator
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
        self.readable: IO[str] = readable
        self.magic_checker: MagicChecker = ObsidianMagicChecker()

    def process_file(self) -> AnkiFileRecord:
        magic = self.magic_checker.get_magic(self.readable)
        if magic is None:
            return AnkiFileRecord("NONE")

        return AnkiFileRecord(magic, self.__get_cards())

    def __get_cards(self) -> Generator[AnkiCard, None, None]:
        while True:
            line = self.readable.readline()
            if line == "":
                return get_empty_anki_generator()

            line = line.strip()
            match = re.match(FileProcessingConstans.BASIC_CARD_REGEX, line)
            if match is None:
                continue

            indentation_level_str: str = match.group(
                FileProcessingConstans.INDENTATION_KEY)

            assert len(indentation_level_str) % 2 == 0
            indentation_level = len(indentation_level_str) // \
                len(FileProcessingConstans.INDENTATION_SEQUENCE)

            front = match.group(
                FileProcessingConstans.FRONT_KEY)

            yield self.__get_basic_card(front, indentation_level)

    def __get_basic_card(self, front: str, indentation_level: int) -> AnkiBasicCard:
        return AnkiBasicCard(front, "backy")
