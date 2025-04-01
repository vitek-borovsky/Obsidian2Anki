### Steps to add support for new card type
- ankiAPI/ankiAPI.py
    - RequestBuilder.add_'new note name'\_note
    - AnkiAPI._create_'new note name'\_card
- AnkiCard.py
    - Create child of AnkiCard and decorate it with @dataclass and name it \*Anki'new note name'Card\*
- repositoryProcessor/FileProcessing.py
    - File.__try_match'new note name' -> \*Anki'new note name'Card\*
- repositoryProcessor/FileProcessingConstants.py
    - Add 'new note name'_CALLOUT
    - Add 'new note name'\_REGEX (build from CALLOUT)

### TODO
better error message when no Vault name supplied
log what cards where created (and how many)
Auto sync after cards created (is this possible???)
Cache what cards were created from which cards and recreate/delete/update them if possible
- Just changed gym -> Gym and it created a new card
- I think I still want to anchor it by ID<->front
