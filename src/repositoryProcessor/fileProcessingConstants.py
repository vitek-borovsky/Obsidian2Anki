class FileProcessingConstans:
    INDENTATION_SEQUENCE = "> "
    INDENTATION_KEY = "INDENTATION"
    FRONT_KEY = "FRONT"

    BASIC_CARD_REGEX = fr"^(?P<{ INDENTATION_KEY }>{INDENTATION_SEQUENCE})+\[!anki\]-(?P<{ FRONT_KEY }>.*)"  # noqa: E501 Flake8 for silence too long of a line

    @staticmethod
    def INDENTATION_MATCHING_REGEX(n: int) -> str:
        """Creates a regex that checks whether a line starts with
        at lest n indentations
        """
        return f"({FileProcessingConstans.INDENTATION_SEQUENCE}){{{n}}}"
