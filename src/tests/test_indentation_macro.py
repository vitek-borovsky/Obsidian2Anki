from ..repositoryProcessor.fileProcessingConstants import FileProcessingConstans

# This test only exits because I'm paranoid about this function
def test_macro_one():
    assert FileProcessingConstans.INDENTATION_MATCHING_REGEX(1) == \
        "(> ){1}"

def test_macro_two():
    assert FileProcessingConstans.INDENTATION_MATCHING_REGEX(2) == \
        "(> ){2}"

def test_macro_three():
    assert FileProcessingConstans.INDENTATION_MATCHING_REGEX(3) == \
        "(> ){3}"
