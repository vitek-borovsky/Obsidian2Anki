from typing import Generator, Self
from functools import singledispatch

from ..ankiCard import AnkiCard, AnkiClasicCard, AnkiFileRecord, AnkiReverseCard, AnkiClozeCard

"""For now we will only use it to create notes"""
class RequestBuilder:
    def __init__(self) -> None:
        self.action = None
        self.notes = []

    def __set_deck_name(self, note: dict, deck_name: str) -> None:
        DECKNAME_KEY = "deckName"
        assert DECKNAME_KEY not in note
        note[DECKNAME_KEY] = deck_name

    def __set_model_name(self, note: dict, model_name: str) -> None:
        MODELNAME_KEY = "modelName"
        assert MODELNAME_KEY not in note
        note[MODELNAME_KEY] = model_name

    def __set_fields(self, note: dict, **kw) -> None:
        FIELDS_KEY = "fields"
        assert FIELDS_KEY not in note
        note[FIELDS_KEY] = kw


    def set_action(self, action: str) -> Self:
        self.action = action
        return self

    def add_basic_note(self, deck_name: str, front: str, back: str) -> Self:
        BASIC_MODEL_NAME = "Basic"
        BASIC_FRONT = "Front"
        BASIC_BACK = "Back"
        note = { }
        self.__set_deck_name(note, deck_name)
        self.__set_model_name(note, BASIC_MODEL_NAME)
        self.__set_fields(note, **{ BASIC_FRONT: front, BASIC_BACK: back })
        self.notes.append(note)
        return self

    def build(self) -> dict:
        ACTION_KEY = "action"
        VERSION_KEY = "version"
        PARAMS_KEY = "params"
        NOTES_KEY = "notes"
        return {
            ACTION_KEY : self.action,
            VERSION_KEY : AnkiAPI.API_VERSION,
            PARAMS_KEY : {
                NOTES_KEY : self.notes
            }
        }


class AnkiAPI:
    TARGET_URL = "http://127.0.0.1"
    TARGET_PORT = 8765
    API_VERSION = 6

    @staticmethod
    def process_file_records(
            anki_file_records: Generator[AnkiFileRecord, None, None]
        ) -> None:
        for file_record in anki_file_records:
            deck_name = file_record.get_deck_name()
            for card in file_record:
                AnkiAPI.__create_card(deck_name, card)

    @singledispatch
    @staticmethod
    def __create_card(deck_name: str, card: AnkiCard) -> None:
        raise RuntimeError("Calling abstract method")

    @__create_card.register(AnkiClasicCard)
    @staticmethod
    def _(deck_name: str, card: AnkiClasicCard) -> None:
        raise NotImplemented

    @__create_card.register(AnkiReverseCard)
    @staticmethod
    def _(deck_name: str, card: AnkiReverseCard) -> None:
        raise NotImplemented

    @__create_card.register(AnkiClozeCard)
    @staticmethod
    def _(deck_name: str, card: AnkiClozeCard) -> None:
        raise NotImplemented
