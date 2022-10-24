import string
import sys


class Document:
    original_text: str
    cleaned_text: str
    k_gram_hashes: list[int]
    k: int # default value is 3 for testing purposes

    def __init__(self, text: str, k: int = 3):
        self.original_text = text
        self.cleaned_text = Document._clean_string(text)
        self.k_gram_hashes = Document._rolling_hash(k, self.cleaned_text)
        self.k = k

    @staticmethod
    def _clean_string(text: str):
        text = text.lower()
        text = "".join(text.split())
        text = text.translate(str.maketrans('', '', string.punctuation))

        return text 

    @staticmethod
    def _rolling_hash(k: int, text: str):
        b = 521 # base
        p = 101 # prime modulus

        k_gram_hashes = []

        hv = 0 # hash value
        for index in range(k-1):
            hv += ord(text[index])
            hv %= p
            hv *= b
            hv %= p
        hv += ord(text[k-1])
        hv %= p

        k_gram_hashes.append(hv)

        lbo = b # left base offset
        for _ in range(k-2):
            lbo = (lbo * b) % p

        i = 0 # index of the leading character
        for index in range(k, len(text)):
            lcv = ord(text[i]) # left char value
            rcv = ord(text[index]) # right char value
            hv = ((hv + p - ((lcv*lbo) % p)) * b + rcv) % p
            k_gram_hashes.append(hv)
            i += 1

        return k_gram_hashes
