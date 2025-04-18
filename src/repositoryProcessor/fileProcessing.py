from typing import IO, Generator
import re
import logging

from .fileProcessingConstants import FileProcessingConstants
from ankiCard import \
    AnkiCard, \
    AnkiBasicCard, \
    AnkiReverseCard, \
    AnkiFileRecord

from .magicChecker import MagicChecker, ObsidianMagicChecker
from config import BASIC_MODEL_NAME, REVERSE_MODEL_NAME


logger = logging.getLogger(__name__)


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
            logger.debug("Magic not found, Exiting file")
            return AnkiFileRecord("NONE")

        logger.info(f"Magic found and is {magic}")
        return AnkiFileRecord(magic, self.__get_cards(magic))

    def __get_cards(self, deck_name: str) -> Generator[AnkiCard, None, None]:
        self.line = self.readable.readline()
        while self.line != "":
            card = self.__try_match_card_header(deck_name)
            if card is not None:
                logger.info(f"Found card in {card.__repr__()}")
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
        return "\n".join(body)

    def __try_match_card_header(self, deck_name: str) -> AnkiCard | None:
        basic_card = self.__try_match_basic_card(deck_name)
        if basic_card is not None:
            return basic_card

        reverse_card = self.__try_match_reverse_card(deck_name)
        if reverse_card is not None:
            return reverse_card
        logger.debug(
            f"Line {self.line.__repr__()} not matched as start of a line")

    def __try_match_basic_card(self, deck_name: str) -> AnkiBasicCard | None:
        regex = FileProcessingConstants.CALLOUT_KEY_TO_REGEX[BASIC_MODEL_NAME]
        match = re.match(regex, self.line)
        if not match:
            return None

        prefix = match.group(FileProcessingConstants.INDENTATION_KEY)
        front = match.group(FileProcessingConstants.FRONT_KEY)
        back = self.__get_lines_while_prefix_matched(prefix)
        return AnkiBasicCard(id=0, deck_name=deck_name, front=front.strip(), back=back.strip())

    def __try_match_reverse_card(self, deck_name: str) -> AnkiReverseCard | None:
        regex = \
            FileProcessingConstants.CALLOUT_KEY_TO_REGEX[REVERSE_MODEL_NAME]
        match = re.match(regex, self.line)
        if not match:
            return None

        prefix = match.group(FileProcessingConstants.INDENTATION_KEY)
        front = match.group(FileProcessingConstants.FRONT_KEY)
        back = self.__get_lines_while_prefix_matched(prefix)
        return AnkiReverseCard(id=0, deck_name=deck_name, front=front.strip(), back=back.strip())
