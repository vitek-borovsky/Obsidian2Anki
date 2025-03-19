from abc import ABC
import re
from typing import IO


class MagicChecker(ABC):
    def get_magic(self, readable: IO[str]) -> str | None:
        raise RuntimeError("Called MagicChecker.check() an abstract class")


class ObsidianMagicChecker(MagicChecker):
    """"""
    METADATA_SEPARATOR = "---"
    ANKI_TAG_KEY = "Anki"
    REGEX_KEY_KEY = "__KEY__"
    REGEX_KEY_VALUE = "__VALUE__"
    KEY_VALUE_REGEX = f"^(?P<{ REGEX_KEY_KEY }>.+):(?P<{ REGEX_KEY_VALUE }>.+)"

    ANKI_SUBFOLDER_SEQUENCE = "::"
    OBSIDIAN_SUBFOLDER_SEQUENCE = "/"

    def get_magic(self, readable: IO[str]) -> str | None:
        """Finding a value of Anki: tag
        Tags are in the header of the file
        Meta data starts and ends with '---'
        between these we are looking for a line
        ANKI_TAG_KEY: ANKI_TAG_VALUE

        :param readable: IO object that has `.readline()` implemented
        :return: The value of a magic or None if not found
        """
        first_line = readable.readline().rstrip()
        if first_line != self.METADATA_SEPARATOR:
            return None

        while True:
            line = readable.readline()
            if line == "":  # EOF
                break
            line = line.rstrip()

            if line == self.METADATA_SEPARATOR:
                break

            match = re.match(self.KEY_VALUE_REGEX, line)
            if match is None:
                continue

            key: str = match.group(self.REGEX_KEY_KEY).strip()
            if key != self.ANKI_TAG_KEY:
                continue

            # Read until we reach the end of metadata
            while True:
                line = readable.readline()
                if line == "":  # EOF
                    break
                line = line.rstrip()
                if line == self.METADATA_SEPARATOR:
                    break

            return match.group(self.REGEX_KEY_VALUE) \
                .strip() \
                .replace(
                    ObsidianMagicChecker.OBSIDIAN_SUBFOLDER_SEQUENCE,
                    ObsidianMagicChecker.ANKI_SUBFOLDER_SEQUENCE)
