from ..ankiAPI.ankiAPI import RequestBuilder
from pprint import pprint

def test_basic():
    request = RequestBuilder() \
        .set_action("addNotes") \
        .add_basic_note("College::PluginDev", "front", "bak" ) \
        .build()

        # This is coppied from the official doccumentation
        # The non-existant model card is removed
        # https://git.sr.ht/~foosoft/anki-connect#card-actions
    CORRECT = {
       "action":"addNotes",
       "version":6,
       "params":{
          "notes":[
             {
                "deckName":"College::PluginDev",
                "modelName":"Basic",
                "fields":{
                   "Front":"front",
                   "Back":"bak"
                }
             }
          ]
       }
    }
    pprint(request)
    pprint(CORRECT)
    assert request == CORRECT
