from typing import Generator, Self
import requests
import json

from ankiCard import \
    AnkiCard, \
    AnkiBasicCard, \
    AnkiFileRecord, \
    AnkiReverseCard, \
    AnkiClozeCard


class RequestBuilder:
    API_VERSION = 6

    ACTION_MULTI = "multi"
    ACTION_CREATE_DECK = "createDeck"
    ACTION_ADD_NOTE = "addNote"

    ACTION_KEY = "action"
    ACTIONS_KEY = "actions"
    VERSION_KEY = "version"
    PARAMS_KEY = "params"
    NOTE_KEY = "note"
    DECK_NAME_KEY = "deckName"
    FIELDS_KEY = "fields"
    MODEL_NAME_KEY = "modelName"

    def __init__(self) -> None:
        self.decks = set()
        self.create_note_action = []

    def __make_note(
            self,
            deck_name: str,
            model_name: str,
            **fields_dict
            ) -> dict:
        self.decks.add(deck_name)
        return {
            self.ACTION_KEY: self.ACTION_ADD_NOTE,
            self.VERSION_KEY: self.API_VERSION,
            self.PARAMS_KEY: {
                self.NOTE_KEY: {
                    self.DECK_NAME_KEY: deck_name,
                    self.MODEL_NAME_KEY: model_name,
                    self.FIELDS_KEY: fields_dict
                }
            }
        }

    def add_basic_note(self, deck_name: str, front: str, back: str) -> Self:
        BASIC_MODEL_NAME = "Basic"
        BASIC_FRONT_KEY = "Front"
        BASIC_BACK_KEY = "Back"

        fields_dict = {
            BASIC_FRONT_KEY: front,
            BASIC_BACK_KEY: back
        }

        note = self.__make_note(
            deck_name,
            BASIC_MODEL_NAME,
            **fields_dict
        )

        self.create_note_action.append(note)
        return self

    def add_reverse_note(self, deck_name: str, front: str, back: str) -> Self:
        REVERSE_MODEL_NAME = "Basic (and reversed card)"
        BASIC_FRONT_KEY = "Front"
        BASIC_BACK_KEY = "Back"

        fields_dict = {
            BASIC_FRONT_KEY: front,
            BASIC_BACK_KEY: back
        }

        note = self.__make_note(
            deck_name,
            REVERSE_MODEL_NAME,
            **fields_dict
        )

        self.create_note_action.append(note)
        return self

    def _build_deck_name(self, deck_name) -> dict:
        DECK_KEY = "deck"
        return {
            self.ACTION_KEY: self.ACTION_CREATE_DECK,
            self.VERSION_KEY: self.API_VERSION,
            self.PARAMS_KEY: {
                DECK_KEY: deck_name
            }
        }

    def build(self) -> dict:
        build_deck_actions = [
            self._build_deck_name(deck_name)
            for deck_name in self.decks
        ]
        #  NOTES_KEY = "notes"
        return {
            self.ACTION_KEY: self.ACTION_MULTI,
            self.VERSION_KEY: self.API_VERSION,
            self.PARAMS_KEY: {
                self.ACTIONS_KEY:
                    build_deck_actions + self.create_note_action
            }
        }


class AnkiAPI:
    def __init__(self) -> None:
        self._request_builder = RequestBuilder()

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
        self._request_builder.add_basic_note(
            deck_name, card.front, card.back)

    def _create_reverse_card(
            self,
            deck_name: str,
            card: AnkiReverseCard
            ) -> None:
        self._request_builder.add_reverse_note(
            deck_name, card.front, card.back)

    def _create_cloze_card(self, deck_name: str, card: AnkiClozeCard) -> None:
        raise NotImplementedError()

    def _get_request(self) -> dict:
        return self._request_builder.build()

    def send_request(self, target_url, target_port) -> requests.Response:
        url = f"{target_url}:{target_port}"
        payload = self._get_request()
        return requests.post(url=url, json=payload)
