from abc import ABC
from dataclasses import dataclass
from typing import Generator

from config import BASIC_MODEL_NAME

"""
Notes will be same if:
- The note is exact match to diffrent note
    - Deck can be diffrent
    - Type can be diffrent

- Deck is still the same
- Type is the same
    - One side of a note is the same
"""

# id: int
# deck_name: str has to be coppied over to all children
# @dataclass officialy sucks

class AnkiCard(ABC):
    id: int
    deck_name: str
    @staticmethod
    def from_response(id: int, body):
        deck_name = body["deckName"]
        model_name = body["modelName"]

        if model_name == BASIC_MODEL_NAME:
            front = body["question"]
            back = body["answer"]
            return AnkiBasicCard(id=id, front=front, back=back, deck_name=deck_name)


        raise NotImplemented("AnkiCard -> Unknown type")

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
    id: int
    deck_name: str
    front: str
    back: str

    def is_almost_same(self, other: AnkiCard) -> bool:
        if not isinstance(other, AnkiBasicCard):
            return super().is_almost_same(other)

        return self.front == other.front or \
               self.back  == other.back

    def __hash__(self) -> int:
        return self.front.__hash__()


@dataclass
class AnkiReverseCard(AnkiCard):
    id: int
    deck_name: str
    front: str
    back: str

    def is_almost_same(self, other: AnkiCard) -> bool:
        if not isinstance(other, AnkiBasicCard):
            return super().is_almost_same(other)

        return self.front == other.front or \
               self.back  == other.back

    def __hash__(self) -> int:
        return self.front.__hash__()

class AnkiClozeCard(AnkiCard):
    deck_name: str

    # def __hash__(self) -> int:
    #     return self.front.__hash__()


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
