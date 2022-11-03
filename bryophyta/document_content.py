from dataclasses import dataclass
import string
import sys


@dataclass
class GlobalPosition:
    index: int
    r: int
    w: int


@dataclass
class Fingerprint:
    val: int
    global_position: GlobalPosition


class DocumentContent:
    original_text: str
    cleaned_text: str
    k_gram_hashes: list[int]
    fingerprints: list[Fingerprint]
    # TODO: give proper default values
    k: int
    w: int

    def __init__(self, text: str, k: int = 50, w: int = 100):
        self.original_text = text
        self.k = k
        self.w = w

        self.cleaned_text = DocumentContent._clean_string(text)
        self.k_gram_hashes = self.rolling_hash()
        self.fingerprints = self.winnow()

    @staticmethod
    def _clean_string(text: str):
        text = text.lower()
        text = "".join(text.split())
        text = text.translate(str.maketrans('', '', string.punctuation))

        return text

    def _val(self, char) -> int:
        return 100 * ord(char)

    def rolling_hash(self):
        # TODO: give proper default values
        b = 23 # base
        p = 2**64 - 1 # prime modulus
        text = self.cleaned_text
        k = self.k

        k_gram_hashes = []

        hv = 0 # hash value
        for index in range(k-1):
            hv += self._val(text[index])
            hv %= p
            hv *= b
            hv %= p
        hv += self._val(text[k-1])
        hv %= p

        k_gram_hashes.append(hv)

        lbo = b # left base offset
        for _ in range(k-2):
            lbo = (lbo * b) % p

        for i, index in enumerate(range(k, len(text))):
            lcv = self._val(text[i]) # left char value
            rcv = self._val(text[index]) # right char value
            hv = ((hv + p - ((lcv*lbo) % p)) * b + rcv) % p
            k_gram_hashes.append(hv)

        return k_gram_hashes

    def winnow(self):
        fingerprints = []
        w = self.w
        h = [sys.maxsize for _ in range(w)]

        r = 0
        min_ = 0

        for i, hash in enumerate(self.k_gram_hashes, start=1):
            r = (r + 1) % w
            h[r] = hash

            if i < w:
                continue

            if min_ == r:
                i = (r - 1) % w
                while i != r:
                    min_ = i if h[i] < h[min_] else min_
                    i = (i - 1 + w) % w
                fingerprints.append(Fingerprint(h[min_], GlobalPosition(min_, r, w)))
            else:
                if h[r] <= h[min_]:
                    min_ = r
                    fingerprints.append(Fingerprint(h[min_], GlobalPosition(min_, r, w)))

        return fingerprints
