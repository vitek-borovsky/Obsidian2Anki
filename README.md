### Steps to add support for new card type
- ankiAPI/ankiAPI.py
    - RequestBuilder.add_<note type name>_note
    - AnkiAPI._create_<note type name>_card
- AnkiCard.py
    - Create child of AnkiCard and decorate it with @dataclass and name it *Anki<note type name>Card*
- repositoryProcessor/FileProcessing.py
    - File.__try_match<note type name> -> *Anki<note type name>Card*
- repositoryProcessor/FileProcessingConstants.py
    - Add <note type name>_CALLOUT
    - Add <note type name>_REGEX (build from CALLOUT)
