from abc import ABC
from typing import IO, TextIO, override


class MagicChecker(ABC):
    def get_magic(self, readable: IO[str]) -> str | None:
        raise RuntimeError("Called MagicChecker.check() an abstract class")

class ObsidianMagicChecker(MagicChecker):
    @override
    def get_magic(self, readable: IO[str]) -> str | None:
        """

        :param readable:
        :type readable:
        :return:
        """
        raise NotImplemented
