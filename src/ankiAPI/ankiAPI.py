from typing import Generator, Self
import requests

from ..ankiCard import \
    AnkiCard, \
    AnkiBasicCard, \
    AnkiFileRecord, \
    AnkiReverseCard, \
    AnkiClozeCard


class RequestBuilder:
    """For now we will only use it to create notes"""
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
        note = {}
        self.__set_deck_name(note, deck_name)
        self.__set_model_name(note, BASIC_MODEL_NAME)
        self.__set_fields(note, **{BASIC_FRONT: front, BASIC_BACK: back})
        self.notes.append(note)
        return self

    def build(self) -> dict:
        ACTION_KEY = "action"
        VERSION_KEY = "version"
        PARAMS_KEY = "params"
        NOTES_KEY = "notes"
        return {
            ACTION_KEY: self.action,
            VERSION_KEY: AnkiAPI.API_VERSION,
            PARAMS_KEY: {
                NOTES_KEY: self.notes
            }
        }


class AnkiAPI:
    API_VERSION = 6

    def __init__(self) -> None:
        self._request_builder = RequestBuilder()
        # TODO this is only for testing
        self._request_builder.set_action("addNotes")

    def process_file_records(
            self,
            anki_file_records: Generator[AnkiFileRecord, None, None]
            ) -> None:
        for file_record in anki_file_records:
            deck_name = file_record.get_deck_name()
            for card in file_record:
                self._create_card(deck_name, card)

    def _create_card(self, deck_name: str, card: AnkiCard) -> None:
        if isinstance(card, AnkiBasicCard):
            self._create_basic_card(deck_name, card)
            return

        if isinstance(card, AnkiReverseCard):
            self._create_reverse_card(deck_name, card)
            return

        if isinstance(card, AnkiClozeCard):
            self._create_cloze_card(deck_name, card)
            return

        raise RuntimeError("Unknown child of AnkiCard")

    def _create_basic_card(self, deck_name: str, card: AnkiBasicCard) -> None:
        self._request_builder.add_basic_note(deck_name, card.front, card.back)

    def _create_reverse_card(
            self,
            deck_name: str,
            card: AnkiReverseCard
            ) -> None:
        raise NotImplementedError()

    def _create_cloze_card(self, deck_name: str, card: AnkiClozeCard) -> None:
        raise NotImplementedError()

    def _get_request(self) -> dict:
         return self._request_builder.build()

    def send_request(self, target_url, target_port) -> None:
        url = f"{target_url}:{target_port}"
        payload = self._get_request()
        requests.post(url=url, json=payload)
