from repositoryProcessor.fileProcessingConstants import \
    FileProcessingConstants


# This test only exits because I'm paranoid about this function
def test_macro_one():
    assert FileProcessingConstants.INDENTATION_MATCHING_REGEX(1) == \
        "(> ){1}"


def test_macro_two():
    assert FileProcessingConstants.INDENTATION_MATCHING_REGEX(2) == \
        "(> ){2}"


def test_macro_three():
    assert FileProcessingConstants.INDENTATION_MATCHING_REGEX(3) == \
        "(> ){3}"
