from abc import ABC
from typing import Generator


class AnkiCard(ABC):
    pass

class AnkiClasicCard(AnkiCard):
    pass

class AnkiReverseCard(AnkiCard):
    pass

class AnkiClozeCard(AnkiCard):
    pass



def get_empty_anki_generator() -> Generator[AnkiCard, None, None]:
    return (_ for _ in [])

class AnkiFileRecord:
    deck_name: str
    cards: Generator[AnkiCard, None, None]

    def __init__(self,
                 deck_name: str,
                 cards: Generator[AnkiCard, None, None] = \
                     get_empty_anki_generator()
             ) -> None:
        self.deck_name = deck_name
        self.cards = cards

    def __iter__(self):
        yield from self.cards

    def get_deck_name(self):
        return self.deck_name
