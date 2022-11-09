from bryophyta.logic.document import Document, Match

def test_combine_matches():
    match1 = Match(1, "the quick brown fox", index=0)
    match2 = Match(1, "fox jumps over the lazy dog", index=16)
    match = Document._combine_matches(match1, match2)
    expected = "the quick brown fox jumps over the lazy dog"
    assert match.matching_text == expected
