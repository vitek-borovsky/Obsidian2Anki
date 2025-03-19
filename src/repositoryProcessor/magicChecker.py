from abc import ABC
import re
from typing import IO


class MagicChecker(ABC):
    def get_magic(self, readable: IO[str]) -> str | None:
        raise RuntimeError("Called MagicChecker.check() an abstract class")


class ObsidianMagicChecker(MagicChecker):
    METADATA_SEPARATOR = "---"
    ANKI_TAG_KEY = "Anki"
    REGEX_KEY_KEY = "__KEY__"
    REGEX_KEY_VALUE = "__VALUE__"
    KEY_VALUE_REGEX = f"^(?P<{ REGEX_KEY_KEY }>.+):(?P<{ REGEX_KEY_VALUE }>.+)"

    ANKI_SUBFOLDER_SEQUENCE = "::"
    OBSIDIAN_SUBFOLDER_SEQUENCE = "/"

    def _is_metadata_start_or_end(self, line: str) -> bool:
        """Expects already striped line of any trailing whitespace

        :param line: line to check
        :return:
        """
        return line == self.METADATA_SEPARATOR

    def _read_till_end_of_metadata(self, readable) -> None:
        while line := readable.readline():
            line = line.rstrip()
            if self._is_metadata_start_or_end(line):
                break

    def get_magic(self, readable: IO[str]) -> str | None:
        """Finding a value of Anki: tag
        Tags are in the header of the file
        Meta data starts and ends with '---'
        between these we are looking for a line
        ANKI_TAG_KEY: ANKI_TAG_VALUE

        :param readable: IO object that has `.readline()` implemented
        :return: The value of a magic or None if not found
        """
        line = readable.readline().rstrip()
        if not self._is_metadata_start_or_end(line):
            return None

        while line := readable.readline():
            line = line.rstrip()
            if self._is_metadata_start_or_end(line):
                break

            match = re.match(self.KEY_VALUE_REGEX, line)
            if match is None:
                continue

            key: str = match.group(self.REGEX_KEY_KEY).strip()
            if key != self.ANKI_TAG_KEY:
                continue

            self._read_till_end_of_metadata(readable)

            return match.group(self.REGEX_KEY_VALUE) \
                .strip() \
                .replace(
                    ObsidianMagicChecker.OBSIDIAN_SUBFOLDER_SEQUENCE,
                    ObsidianMagicChecker.ANKI_SUBFOLDER_SEQUENCE)
