from dataclasses import dataclass, field

from bryophyta.logic.document_content import DocumentContent, Fingerprint


class Match:
    document_id: int
    matching_text: str
    fingerprint: Fingerprint = None
    iindex: int = None

    def __init__(
        self,
        document_id: int,
        matching_text: str,
        fingerprint: Fingerprint = None,
        index: int = None
    ):
        self.document_id = document_id
        self.matching_text = matching_text
        self.fingerprint = fingerprint
        self.iindex = index


    @property
    def index(self):
        return self.iindex or self.fingerprint.global_position.index

    @property
    def length(self):
        return len(self.matching_text)


class Document:
    id: int
    title: str
    content: DocumentContent
    matches: list[Match]
    percent_match: float = 0.0

    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.content = DocumentContent(body)
        self.matches = []

    def get_matching_text(self, fingerprint: Fingerprint) -> str:
        i = fingerprint.global_position.index
        length = self.content.k

        return self.content.cleaned_text[i:i+length]


    #TODO: deal with matches that are close but do not overlap...
    # this needs to be done with consideration to the documents
    # it's matching with though... in the future
    def _group_overlapping_matches(self) -> list[list[Match]]:
        if len(self.matches) <= 1:
            return []

        self.matches.sort(key=lambda x: x.index)
        overlaps = []
        group = []

        for i in range(len(self.matches) - 1):
            group.append(self.matches[i])

            if not self._matches_overlap(self.matches[i], self.matches[i+1]):
                if len(group) > 1:
                    overlaps.append(group)
                group = []

        if self._matches_overlap(self.matches[-2], self.matches[-1]):
            try:
                overlaps[-1].append(self.matches[-1])
            except KeyError:
                overlaps.append(self.matches[-2], self.matches[-1])

        return overlaps

    @staticmethod
    def _matches_overlap(match1: Match, match2: Match):
        return match1.index + match1.length >= match2.index

    def _combine_matches(self, overlaps: list[list[Match]]):
        self.matches = []

        for group in overlaps:
            match = self._combine_match(group[0], group[1])
            #TODO: fix this grossness
            for i in range(2, len(group)):
                match = self._combine_match(match, group[i])

            self.matches.append(match)

    @staticmethod
    def _combine_match(match1: Match, match2: Match) -> Match:
        diff = match2.index - match1.index
        matching_text = match1.matching_text + match2.matching_text[-diff:]

        return Match(match1.document_id, matching_text, index=match1.index)

    def combine_matches(self):
        self._combine_matches(self._group_overlapping_matches())
