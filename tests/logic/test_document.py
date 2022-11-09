from bryophyta.logic.document import Document, Match
from tests.utils import generate_random_string


def test_combine_matches():
    match1 = Match(1, "the quick brown fox", index=0)
    match2 = Match(1, "fox jumps over the lazy dog", index=16)
    match = Document._combine_matches(match1, match2)
    expected = "the quick brown fox jumps over the lazy dog"
    assert match.matching_text == expected


def test_group_matches():
    text = generate_random_string(1000)
    document = Document(1, "foo", text)
    match1 = Match(1, "the quick brown fox", index=0)
    match2 = Match(1, "fox jumps over the lazy dog", index=16)
    match3 = Match(1, "g and has lots of fun", index=42)
    document.matches = [match1, match2, match3]
    document.combine_matches()
    assert len(document.matches) == 1
    expected = "the quick brown fox jumps over the lazy dog and has lots of fun"
    assert document.matches[0].matching_text == expected
