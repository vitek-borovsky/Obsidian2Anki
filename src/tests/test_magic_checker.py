import pytest
from io import StringIO

from ..repositoryProcessor.magicChecker import ObsidianMagicChecker

ANKI_KEY = ObsidianMagicChecker.ANKI_TAG_KEY

@pytest.fixture
def checker():
    return ObsidianMagicChecker()


#TODO better names for tests
#TODO more tests

### MAGIC SHOULD BE DETECTED
@pytest.mark.parametrize("string, value", [
    (f"""---
{ANKI_KEY}: TARGET DECK
---
    """,  "TARGET DECK")
])
def test_possitive(checker: ObsidianMagicChecker, string, value):
    readable = StringIO(string)
    assert checker.get_magic(readable) == value


@pytest.mark.parametrize("string, value", [
    (f"""---
Anki: TARGET DECK
Anki: OTHER DECK
---
    """, "TARGET DECK")
])
def test_multiple_anki_tags(checker, string, value):
    readable = StringIO(string)
    assert checker.get_magic(readable) == value

### NO MAGIC SHOULD BE DETECTED
@pytest.mark.parametrize("string", [
    (f"""---
SOME_TAG: TARGET DECK
---
    """)
])
def test_negative(checker, string):
    readable = StringIO(string)
    assert checker.get_magic(readable) is None

@pytest.mark.parametrize("string", [
    (f"""---
SOME_TAG: TARGET DECK
---
Anki: TARGET_DECK
    """)
])
def test_tag_beyond_metadata_not_detected(checker, string):
    readable = StringIO(string)
    assert checker.get_magic(readable) is None
