from bryophyta.logic.document_content import DocumentContent
from tests.utils import generate_random_string


def test_clean_text():
    document = DocumentContent("A do run run run, a do run run", k=3, w=4)
    assert document.cleaned_text == "adorunrunrunadorunrun"


def test_rolling_hash():
    document = DocumentContent("abracadabra", k=3, w=4)
    hashes = document.k_gram_hashes
    assert hashes[0] == hashes[7]
    assert hashes[1] == hashes[8]


def test_rolling_hash_distribution():
    text = generate_random_string(50_000)
    document = DocumentContent(text)
    average_hash = sum(document.k_gram_hashes) / len(document.k_gram_hashes)
    expected_average = (2**64 - 1) / 2
    assert average_hash > expected_average * 0.90
    assert average_hash < expected_average * 1.10


def test_winnow():
    document = DocumentContent("A do run run run, a do run run", k=3, w=4)
    document.k_gram_hashes = [77, 74, 42, 17, 98, 50, 17, 98, 8, 88, 67, 39, 77, 74, 42, 17, 98]
    document.fingerprints = document.winnow()
    fingerprints = [f.val for f in document.fingerprints]
    expected = [17, 17, 8, 39, 17]
    assert fingerprints == expected
