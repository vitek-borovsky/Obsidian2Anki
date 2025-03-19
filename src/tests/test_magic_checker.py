import pytest
from io import StringIO

from ..repositoryProcessor.magicChecker import ObsidianMagicChecker

ANKI_KEY = ObsidianMagicChecker.ANKI_TAG_KEY


@pytest.fixture
def checker():
    return ObsidianMagicChecker()


# TODO better names for tests
# TODO more tests

# MAGIC SHOULD BE DETECTED
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
{ANKI_KEY}: TARGET DECK
{ANKI_KEY}: OTHER DECK
---
    """, "TARGET DECK")
])
def test_multiple_anki_tags(checker, string, value):
    readable = StringIO(string)
    assert checker.get_magic(readable) == value


# NO MAGIC SHOULD BE DETECTED
@pytest.mark.parametrize("string", [
    ("""---
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
{ANKI_KEY}: TARGET_DECK
    """)
])
def test_tag_beyond_metadata_not_detected(checker, string):
    readable = StringIO(string)
    assert checker.get_magic(readable) is None


@pytest.mark.parametrize("string, deck_name", [
    (f"""---
{ANKI_KEY}: TARGET DECK/SUB DECK
---
    """, "TARGET DECK::SUB DECK")
])
def test_sub_deck(checker, string, deck_name):
    readable = StringIO(string)
    magic = checker.get_magic(readable)
    assert magic == deck_name


@pytest.mark.parametrize("string, deck_name", [
    (f"""---
{ANKI_KEY}: TARGET DECK
""", "TARGET DECK")
])
def test_metadata_not_closed_with_match(checker, string, deck_name):
    readable = StringIO(string)
    magic = checker.get_magic(readable)
    assert magic == deck_name


@pytest.mark.parametrize("string", [
    ("""---
SOME_TAG: TARGET DECK
""")
])
def test_metadata_not_closed_with_no_match(checker, string):
    readable = StringIO(string)
    magic = checker.get_magic(readable)
    assert magic is None
