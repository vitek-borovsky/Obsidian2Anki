from abc import ABC
from dataclasses import dataclass
from typing import Generator

"""
Notes will be same if:
- The note is exact match to diffrent note
    - Deck can be diffrent
    - Type can be diffrent

- Deck is still the same
- Type is the same
    - One side of a note is the same
"""



class AnkiCard(ABC):
    def is_almost_same(self, other) -> bool:
        """
        Checks if two notes are "same" i.e. some callout in vault was updated
        """
        if not other is AnkiCard:
            return False
        #TODO implement Basic <-> Basic and reversed change
        return False


@dataclass
class AnkiBasicCard(AnkiCard):
    front: str
    back: str

    def is_almost_same(self, other: AnkiCard) -> bool:
        if not isinstance(other, AnkiBasicCard):
            return super().is_almost_same(other)

        return self.front == other.front or \
               self.back  == other.back


@dataclass
class AnkiReverseCard(AnkiCard):
    front: str
    back: str

    def is_almost_same(self, other: AnkiCard) -> bool:
        if not isinstance(other, AnkiBasicCard):
            return super().is_almost_same(other)

        return self.front == other.front or \
               self.back  == other.back


class AnkiClozeCard(AnkiCard):
    pass


def get_empty_anki_generator() -> Generator[AnkiCard, None, None]:
    return (_ for _ in [])


class AnkiFileRecord:
    _deck_name: str
    cards: Generator[AnkiCard, None, None]

    def __init__(
            self,
            deck_name: str,
            cards: Generator[AnkiCard, None, None] = get_empty_anki_generator()
             ) -> None:
        self._deck_name = deck_name
        self.cards = cards

    def __repr__(self) -> str:
        return f"AnkiFileRecord({self._deck_name})"

    def __iter__(self):
        yield from self.cards

    def get_deck_name(self):
        return self._deck_name
