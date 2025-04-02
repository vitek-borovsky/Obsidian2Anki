from typing import Generator
import requests
import logging

from ankiCard import \
    AnkiCard, \
    AnkiBasicCard, \
    AnkiFileRecord, \
    AnkiReverseCard, \
    AnkiClozeCard

from caching import Action, AnkiIDCache
from config import BASIC_MODEL_NAME, REVERSE_MODEL_NAME


logger = logging.getLogger(__name__)


class AnkiAPI:
    def __init__(self, target_url, target_port) -> None:
        self.target = f"{target_url}:{target_port}"
        self.available_decks = self._get_decks()
        self.id_cacher = AnkiIDCache(self)

    def get_notes_by_id(self, ids: list[int]):
        payload = {
            "action": "cardsInfo",
            "version": 6,
            "params": {
                "cards": ids
            }
        }
        return self._send_request(payload).json()["result"]

    def process_file_records(
            self,
            anki_file_records: Generator[AnkiFileRecord, None, None]
            ) -> None:
        for file_record in anki_file_records:
            deck_name = file_record.get_deck_name()
            self._process_file_record(file_record, deck_name)

    def _process_file_record(self, file_record: AnkiFileRecord, deck_name: str) -> None:
        for card in file_record:
            action = self.id_cacher.get(deck_name, card)
            match action:
                case Action.CREATE:
                    self._create_card(deck_name, card)
                case Action.UPDATE:
                    pass # TODO
                case Action.NO_ACTION:
                    pass
                case _:
                    raise NotImplemented("Unknown Action")

    def _get_decks(self) -> list[str]:
        payload = {
            "action": "deckNames",
            "version": 6
        }
        self._send_request(payload)
        return []

    def _make_deck_available(self, deck_name: str) -> None:
        if deck_name in self.available_decks:
            return

        payload = {
            "action": "createDeck",
            "version": 6,
            "params": {
                "deck": deck_name
            }
        }
        self._send_request(payload)
        self.available_decks.append(deck_name)

    def _create_card(self, deck_name: str, card: AnkiCard) -> None:
        self._make_deck_available(deck_name)

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
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": BASIC_MODEL_NAME,
                    "fields": {
                        "Front": card.front,
                        "Back": card.back,
                    },
                }
            }
        }
        logger.debug(f"Creating basic card {payload}")
        self._send_request(payload)

    def _create_reverse_card(
            self,
            deck_name: str,
            card: AnkiReverseCard
            ) -> None:
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": REVERSE_MODEL_NAME,
                    "fields": {
                        "Front": card.front,
                        "Back": card.back,
                    },
                }
            }
        }
        logger.debug(f"Creating reverse card {payload}")
        self._send_request(payload)

    def _create_cloze_card(self, deck_name: str, card: AnkiClozeCard) -> None:
        raise NotImplementedError()

    def _send_request(self, payload: dict) -> requests.Response:
        return requests.post(url=self.target, json=payload)
