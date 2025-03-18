from typing import Generator
from functools import singledispatch

from ankiCard import AnkiCard, AnkiClasicCard, AnkiFileRecord, AnkiReverseCard, AnkiClozeCard


class AnkiAPI:
    @staticmethod
    def process_file_records(
            anki_file_records: Generator[AnkiFileRecord, None, None]
        ) -> None:
        for file_record in anki_file_records:
            deck_name = file_record.get_deck_name()
            for card in file_record:
                AnkiAPI.create_card(deck_name, card)

    @staticmethod
    @singledispatch
    def create_card(deck_name: str, card: AnkiCard) -> None:
        raise RuntimeError("Calling abstract method")

    @staticmethod
    @create_card.register(AnkiClasicCard)
    def _(deck_name: str, card: AnkiClasicCard) -> None:
        raise NotImplemented

    @staticmethod
    @create_card.register(AnkiReverseCard)
    def _(deck_name: str, card: AnkiReverseCard) -> None:
        raise NotImplemented

    @staticmethod
    @create_card.register(AnkiClozeCard)
    def _(deck_name: str, card: AnkiClozeCard) -> None:
        raise NotImplemented
