from typing import IO, Generator
import re

from .fileProcessingConstants import FileProcessingConstants
from ankiCard import \
    AnkiCard, \
    AnkiBasicCard, \
    AnkiReverseCard, \
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
        while self.line != "":
            card = self.__try_match_card_header()
            if card is not None:
                yield card

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

    def __try_match_card_header(self) -> AnkiCard | None:
        basic_card = self.__try_match_basic_card()
        if basic_card is not None:
            return basic_card

        reverse_card = self.__try_match_reverse_card()
        if reverse_card is not None:
            return reverse_card

    def __try_match_basic_card(self) -> AnkiBasicCard | None:
        match = re.match(FileProcessingConstants.REVERSE_CARD_REGEX, self.line)
        if not match:
            return None

        prefix = match.group(FileProcessingConstants.INDENTATION_KEY)
        front = match.group(FileProcessingConstants.FRONT_KEY)
        back = self.__get_lines_while_prefix_matched(prefix)
        return AnkiBasicCard(front.strip(), back.strip())

    def __try_match_reverse_card(self) -> AnkiReverseCard | None:
        match = re.match(FileProcessingConstants.BASIC_CARD_REGEX, self.line)
        if not match:
            return None

        prefix = match.group(FileProcessingConstants.INDENTATION_KEY)
        front = match.group(FileProcessingConstants.FRONT_KEY)
        back = self.__get_lines_while_prefix_matched(prefix)
        return AnkiReverseCard(front.strip(), back.strip())
