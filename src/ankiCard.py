from abc import ABC, abstractmethod
from typing import Generator

from config import BASIC_MODEL_NAME, REVERSE_MODEL_NAME

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
    id: int
    deck_name: str

    def __init__(self, id: int, deck_name: str) -> None:
        self.id = id
        self.deck_name = deck_name

    @abstractmethod
    def match_data(self, other) -> bool:
        raise NotImplemented("This method should be overwritten")

    @staticmethod
    def from_response(deck_name: str, body):
        import pdb; pdb.set_trace()
        if body == {}:
            return

        id = body["noteId"]
        model_name = body["modelName"]

        if model_name == BASIC_MODEL_NAME:
            front = body["fields"]["Front"]["value"]
            back = body["fields"]["Back"]["value"]
            return AnkiBasicCard(id=id, front=front, back=back, deck_name=deck_name)

        if model_name == REVERSE_MODEL_NAME:
            front = body["question"]
            back = body["answer"]
            return AnkiReverseCard(id=id, front=front, back=back, deck_name=deck_name)

        raise NotImplemented(f"AnkiCard -> Unknown type {model_name}")

    def is_almost_same(self, other) -> bool:
        """
        Checks if two notes are "same" i.e. some callout in vault was updated
        """
        if not other is AnkiCard:
            return False

        #TODO implement Basic <-> Basic and reversed change
        if (isinstance(self, AnkiBasicCard) and isinstance(other, AnkiReverseCard)) or \
           (isinstance(other, AnkiBasicCard) and isinstance(self, AnkiReverseCard)):
            if self.deck_name == other.deck_name and \
                self.front == other.front and \
                self.back == other.back:
                return True
        return False



class AnkiBasicCard(AnkiCard):
    front: str
    back: str

    def __init__(self, id: int, deck_name: str, front: str, back: str) -> None:
        self.front = front
        self.back = back
        super().__init__(id, deck_name)

    def __repr__(self) -> str:
        return f"AnkiBasicCard({self.id}, {self.deck_name}, {self.front.__repr__()}, {self.back.__repr__()})"

    def match_data(self, other) -> bool:
        return self.front == other.front and \
            self.back == other.back

    def is_almost_same(self, other: AnkiCard) -> bool:
        if not isinstance(other, AnkiBasicCard):
            return super().is_almost_same(other)

        return self.front == other.front or \
               self.back  == other.back

    def __hash__(self) -> int:
        return self.front.__hash__()


class AnkiReverseCard(AnkiCard):
    def __init__(self, id: int, deck_name: str, front: str, back: str) -> None:
        self.front = front
        self.back = back
        super().__init__(id, deck_name)

    def __repr__(self) -> str:
        return f"AnkiReverseCard({self.id}, {self.deck_name}, {self.front.__repr__()}, {self.back.__repr__()})"

    def match_data(self, other) -> bool:
        return self.front == other.front and \
            self.back == other.back

    def is_almost_same(self, other: AnkiCard) -> bool:
        # If the cards have diffrent deck , they must be exact match
        if self.deck_name != other.deck_name:
            return self.match_data(other)

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
    deck_name: str
    cards: Generator[AnkiCard, None, None]

    def __init__(
            self,
            deck_name: str,
            cards: Generator[AnkiCard, None, None] = get_empty_anki_generator()
             ) -> None:
        self.deck_name = deck_name
        self.cards = cards

    def __repr__(self) -> str:
        return f"AnkiFileRecord({self.deck_name})"

    def __iter__(self):
        yield from self.cards
