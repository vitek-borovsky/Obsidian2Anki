from pathlib import Path
from queue import Queue
from typing import Generator

from ankiCard import AnkiFileRecord
from .fileProcessing import File


class RepositoryProcessor:
    def __init__(self, repository_root: Path) -> None:
        self.repository_root = repository_root

    def execute(self) -> Generator[AnkiFileRecord]:
        subfolders: Queue[Path] = Queue()
        subfolders.put(self.repository_root)

        while not subfolders.empty():
            current_folder: Path = subfolders.get()

            for file in current_folder.iterdir():
                if file.is_dir():
                    subfolders.put(file)
                    continue

                with open(file) as readable:
                    yield File(readable).process_file()
