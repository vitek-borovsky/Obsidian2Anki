class FileProcessingConstants:
    INDENTATION_SEQUENCE = "> "
    INDENTATION_KEY = "INDENTATION"
    FRONT_KEY = "FRONT"

    CALLOUT_KEY_TO_REGEX: dict[str, str] = {}

    @staticmethod
    def set_up(callout_to_card_types: dict[str, list[str]]) -> None:
        FileProcessingConstants.CALLOUT_KEY_TO_REGEX = {
            key: FileProcessingConstants.__get_callout_regex(callout_keys)
            for key, callout_keys in callout_to_card_types.items()
        }

    @staticmethod
    def __get_callout_regex(callout_keys: list[str]) -> str:
        """Matches
        '> ' any amount of times and matches it as INDENTATION_KEY
        [!<key>]
        followed by possibly '+' or '-'
        then skips ONE SPACE and matches rest as
        matches rest of the line with FRONT_KEY
        """
        REGEX_OR_CHAR = "|"
        callout_keys_regex = REGEX_OR_CHAR.join(callout_keys)
        indentation = fr"(?P<{ FileProcessingConstants.INDENTATION_KEY }>{FileProcessingConstants.INDENTATION_SEQUENCE})+"  # noqa: 501
        main_body = fr"\[!{callout_keys_regex}\][-+]?"
        front_capture = fr" (?P<{ FileProcessingConstants.FRONT_KEY }>.*)"
        return f"{indentation}{main_body}{front_capture}"

    @staticmethod
    def INDENTATION_MATCHING_REGEX(n: int) -> str:
        """Creates a regex that checks whether a line starts with
        at lest n indentations
        """
        return f"({FileProcessingConstants.INDENTATION_SEQUENCE}){{{n}}}"
