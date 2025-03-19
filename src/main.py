from pathlib import Path
from ankiAPI.ankiAPI import AnkiAPI
from repositoryProcessor.repositoryProcessor import RepositoryProcessor
# from sys import argv

if __name__ == '__main__':
    # repository_root = argv[1]
    repository_root = Path("./test-vault")
    repository_processor = RepositoryProcessor(repository_root)
    file_records = repository_processor.execute()


    TARGET_URL = "http://127.0.0.1"
    TARGET_PORT = 8765

    anki_api = AnkiAPI()
    anki_api.process_file_records(file_records)
    request = anki_api.send_request(TARGET_URL, TARGET_PORT)
