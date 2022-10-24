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
