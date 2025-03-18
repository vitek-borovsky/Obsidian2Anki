from pathlib import Path
from repositoryProcessor.repositoryProcessor import RepositoryProcessor
# from sys import argv

if __name__ == '__main__':
    # repository_root = argv[1]
    repository_root = Path("./test-vault")
    repository_processor = RepositoryProcessor(repository_root)
    repository_processor.execute()
