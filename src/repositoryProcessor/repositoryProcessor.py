from pathlib import Path
from queue import Queue
from typing import Generator
import logging

from ankiCard import AnkiFileRecord
from .fileProcessing import File


logger = logging.getLogger(__name__)


class RepositoryProcessor:
    DESIRED_SUFFIXES = [".md"]

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root

    def execute(self) -> Generator[AnkiFileRecord, None, None]:
        subfolders: Queue[Path] = Queue()
        subfolders.put(self.repository_root)

        while not subfolders.empty():
            current_folder: Path = subfolders.get()
            logger.debug(f"Processing subfolder {current_folder}")

            for file in current_folder.iterdir():
                logger.debug(f"Processing file {file.name}")
                if file.is_dir():
                    logger.debug("File is a directory")
                    subfolders.put(file)
                    continue

                if file.suffix not in self.DESIRED_SUFFIXES:
                    logger.debug(f"File does not match by extension {file.suffix}")
                    continue

                with open(file, 'r') as readable:
                    logger.info(f"Processing file {file}")
                    yield File(readable).process_file()
