#!/usr/bin/env python
import sys
import logging

from pathlib import Path
from ankiAPI.ankiAPI import AnkiAPI
from repositoryProcessor.repositoryProcessor import RepositoryProcessor


logger = logging.getLogger(__name__)


def main(
        vault_root: str,
        TARGET_URL: str = "http://127.0.0.1",
        TARGET_PORT: int = 8765
        ) -> None:
    logging.basicConfig(filename='ObsidianToAnki.log', level=logging.DEBUG)

    logger.info(f"Runing on Vault:'{vault_root}'")

    repository_processor = RepositoryProcessor(Path(vault_root))
    file_records = repository_processor.execute()

    anki_api = AnkiAPI(TARGET_URL, TARGET_PORT)
    anki_api.process_file_records(file_records)


if __name__ == '__main__':
    vault_dir = sys.argv[1]
    main(vault_dir)
