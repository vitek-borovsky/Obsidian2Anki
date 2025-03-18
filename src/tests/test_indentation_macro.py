from ..repositoryProcessor.fileProcessingConstants import FileProcessingConstatns

# This test only exits because I'm paranoid about this function
def test_macro_one():
    assert FileProcessingConstatns.INDENTATION_MATCHING_REGEX(1) == \
        "(> ){1}"

def test_macro_two():
    assert FileProcessingConstatns.INDENTATION_MATCHING_REGEX(2) == \
        "(> ){2}"

def test_macro_three():
    assert FileProcessingConstatns.INDENTATION_MATCHING_REGEX(3) == \
        "(> ){3}"
