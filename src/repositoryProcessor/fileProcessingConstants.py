class FileProcessingConstants:
    INDENTATION_SEQUENCE = "> "
    INDENTATION_KEY = "INDENTATION"
    FRONT_KEY = "FRONT"

    BASIC_CARD_CALLOUT = "anki"
    REVERSE_CARD_CALLOUT = "ankiR"

    BASIC_CARD_REGEX = fr"^(?P<{ INDENTATION_KEY }>{INDENTATION_SEQUENCE})+\[!{BASIC_CARD_CALLOUT}\][-+]? (?P<{ FRONT_KEY }>.*)"  # noqa: E501 Flake8 for silence too long of a line
    REVERSE_CARD_REGEX = fr"^(?P<{ INDENTATION_KEY }>{INDENTATION_SEQUENCE})+\[!{REVERSE_CARD_CALLOUT}\][-+]? (?P<{ FRONT_KEY }>.*)"  # noqa: E501

    @staticmethod
    def INDENTATION_MATCHING_REGEX(n: int) -> str:
        """Creates a regex that checks whether a line starts with
        at lest n indentations
        """
        return f"({FileProcessingConstants.INDENTATION_SEQUENCE}){{{n}}}"
