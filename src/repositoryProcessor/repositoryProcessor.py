from pathlib import Path
from queue import Queue
from typing import Generator

from ankiCard import AnkiFileRecord
from .fileProcessing import File


class RepositoryProcessor:
    DESIRED_SUFFIXES = [".md"]

    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root

    def execute(self) -> Generator[AnkiFileRecord, None, None]:
        subfolders: Queue[Path] = Queue()
        subfolders.put(self.repository_root)

        while not subfolders.empty():
            current_folder: Path = subfolders.get()

            for file in current_folder.iterdir():
                if file.is_dir():
                    subfolders.put(file)
                    continue

                if file.suffix not in self.DESIRED_SUFFIXES:
                    continue

                with open(file, 'r') as readable:
                    yield File(readable).process_file()
