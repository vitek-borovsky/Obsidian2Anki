#!/usr/bin/env python
import sys
import json

from pathlib import Path
from ankiAPI.ankiAPI import AnkiAPI
from repositoryProcessor.repositoryProcessor import RepositoryProcessor


def main(
        vault_root: str,
        TARGET_URL: str = "http://127.0.0.1",
        TARGET_PORT: int = 8765
        ) -> None:
    repository_processor = RepositoryProcessor(Path(vault_root))
    file_records = repository_processor.execute()

    anki_api = AnkiAPI()
    anki_api.process_file_records(file_records)
    response = anki_api.send_request(TARGET_URL, TARGET_PORT)
    response_json = json.dumps(response.json())
    print()
    print(response_json)


if __name__ == '__main__':
    vault_dir = sys.argv[1]
    main(vault_dir)
