import pytest
from io import StringIO

from repositoryProcessor.fileProcessing import File
from ankiCard import AnkiBasicCard, AnkiReverseCard


@pytest.mark.parametrize("string", [
    ("""---
Anki: Target Deck
---
astnoinsatiast

ast
as
r
satr
asrt
""")
])
def test_magic_detection(string):
    readable = StringIO(string)
    f = File(readable)
    afr = f.process_file()

    assert afr.get_deck_name() == "Target Deck"


@pytest.mark.parametrize("string", [
    ("""---
Anki: Target Deck
---
astnoinsatiast

ast
as
r
satr
asrt
""")
])
def test_no_match(string):
    readable = StringIO(string)
    f = File(readable)
    afr = f.process_file()

    cards = list(afr.cards)
    assert cards == []


@pytest.mark.parametrize("string", [
    ("""---
Anki: Target Deck
> [!anki] This is front
> This is back
---
astnoinsatiast

ast
as
r
asrt
""")
])
def test_match_in_metadata_not_detected(string):
    readable = StringIO(string)
    f = File(readable)
    afr = f.process_file()

    cards = list(afr.cards)
    assert cards == []


@pytest.mark.parametrize("string", [
    ("""---
Anki: Target Deck
---
astnoinsatiast

ast
as
r
> [!anki] This is front
> This is back
asrt
""")
])
def test_match_basic_card(string):
    readable = StringIO(string)
    f = File(readable)
    afr = f.process_file()

    cards = list(afr.cards)
    assert cards == [AnkiBasicCard("This is front", "This is back")]


@pytest.mark.parametrize("string", [
    ("""---
Anki: Target Deck
---
astnoinsatiast

ast
as
r
> [!ankiR] This is front
> This is back
asrt
""")
])
def test_match_reverse_card(string):
    readable = StringIO(string)
    f = File(readable)
    afr = f.process_file()

    cards = list(afr.cards)
    assert cards == [AnkiReverseCard("This is front", "This is back")]
