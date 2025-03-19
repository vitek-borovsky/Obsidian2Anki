from typing import IO, Generator
import re

from .fileProcessingConstants import FileProcessingConstants
from ankiCard import \
    AnkiCard, \
    AnkiBasicCard, \
    AnkiFileRecord

from .magicChecker import MagicChecker, ObsidianMagicChecker


class File:
    """Represent open file in memory
    File is proccessed as followed
    - Metadata is read and checked for magic,
      if no magic is present we exit
    - Read and store target deck name
    - Process the rest of the file and create AnkiCard objects
    """
    def __init__(self, readable: IO[str]) -> None:
        self.readable: IO[str] = readable
        self.magic_checker: MagicChecker = ObsidianMagicChecker()
        self.line = ""

    def process_file(self) -> AnkiFileRecord:
        magic = self.magic_checker.get_magic(self.readable)
        if magic is None:
            return AnkiFileRecord("NONE")

        return AnkiFileRecord(magic, self.__get_cards())

    def __get_cards(self) -> Generator[AnkiCard, None, None]:
        self.line = self.readable.readline()
        while True:
            if self.line == "":
                return None

            basic_card = self.__try_match_basic_card()
            if basic_card is not None:
                yield basic_card
                continue

            self.line = self.readable.readline()

    def __get_lines_while_prefix_matched(self, prefix: str) -> str:
        """Expects first(front) line to be already read and matched """
        body = []
        while True:
            self.line = self.readable.readline()
            if self.line == "":  # EOF
                break

            if not self.line.startswith(prefix):
                break

            body.append(self.line.removeprefix(prefix))
        return "".join(body)

    def __try_match_basic_card(self) -> AnkiCard | None:
        match = re.match(FileProcessingConstants.BASIC_CARD_REGEX, self.line)
        if not match:
            return None

        prefix = match.group(FileProcessingConstants.INDENTATION_KEY)
        front = match.group(FileProcessingConstants.FRONT_KEY)
        back = self.__get_lines_while_prefix_matched(prefix)
        return AnkiBasicCard(front.strip(), back.strip())
