#!/usr/bin/env sh
cd $(dirname $0)

set -eu

curl -X POST http://127.0.0.1:8765 \
    -H "Content-Type: application/json" \
    -d '{
      "action": "loadProfile",
      "version": 6,
      "params": {
        "name": "Tester"
    }' &> /dev/null ||:

mv ~/.cache/ObsidianToAnki/AnkiIdCache.pkl ~/.cache/ObsidianToAnki/AnkiIdCache.pkl.bak ||:

(rm ObsidianToAnki.log ||:) &> /dev/null

curl -X POST http://127.0.0.1:8765 \
     -H "Content-Type: application/json" \
     -d '{
         "action": "deleteDecks",
         "version": 6,
         "params": {
             "decks": ["Test"],
             "cardsToo": true
         }
     }' &> /dev/null ||:

PYTHONPATH=../../ python manual_invoke.py "./Vault"
PYTHONPATH=../../ python manual_invoke.py "./VaultChanged"


# curl -X POST http://127.0.0.1:8765 \
#     -H "Content-Type: application/json" \
#     -d '{
#     "action": "loadProfile",
#     "version": 6,
#     "params": {
#         "name": "Vitek"
#     }' &> /dev/null ||:
mv ~/.cache/ObsidianToAnki/AnkiIdCache.pkl.bak ~/.cache/ObsidianToAnki/AnkiIdCache.pkl ||:
