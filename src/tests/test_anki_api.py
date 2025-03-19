from ..ankiCard import AnkiFileRecord, AnkiBasicCard
from ..ankiAPI.ankiAPI import RequestBuilder, AnkiAPI
from pprint import pprint


# This is coppied from the official doccumentation
# The non-existant model card is removed
# https://git.sr.ht/~foosoft/anki-connect#card-actions
CORRECT = {
   "action": "addNotes",
   "version": 6,
   "params": {
      "notes": [
         {
            "deckName": "College::PluginDev",
            "modelName": "Basic",
            "fields": {
               "Front": "front",
               "Back": "bak"
            }
         }
      ]
   }
}


def test_request_builder():
    request = RequestBuilder() \
        .set_action("addNotes") \
        .add_basic_note("College::PluginDev", "front", "bak") \
        .build()

    pprint(request)
    pprint(CORRECT)
    assert request == CORRECT
