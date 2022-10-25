import unittest

from bryophyta.document import Document


class Test(unittest.TestCase):
    def test_clean_text(self):
        document = Document("A do run run run, a do run run")

        self.assertEqual(document.cleaned_text, "adorunrunrunadorunrun")


    def test_rolling_hash(self):
        document = Document("abracadabra")

        hashes = document.k_gram_hashes

        self.assertEqual(hashes[0], hashes[7])
        self.assertEqual(hashes[1], hashes[8])

    def test_winnow(self):
        document = Document("A do run run run, a do run run", w=4)

        document.k_gram_hashes = [77, 74, 42, 17, 98, 50, 17, 98, 8, 88, 67, 39, 77, 74, 42, 17, 98]
        document.winnow()

        fingerprints = [f.val for f in document.fingerprints]
        expected = [17, 17, 8, 39, 17]

        self.assertListEqual(fingerprints, expected)
