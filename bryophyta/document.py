from dataclasses import dataclass, field

from bryophyta.document_content import DocumentContent, Fingerprint


@dataclass
class Author:
    name: str


@dataclass
class Match:
    fingerprint: Fingerprint
    matching_document_names: list[str]
    matching_text: str


@dataclass
class Document:
    name: str
    author: Author
    content: DocumentContent
    matches: list[Match] = field(default_factory=list)
    percent_match: float = 0.0


    def get_matching_text(self, fingerprint: Fingerprint) -> str:
        i = fingerprint.global_position.index
        length = self.content.k

        return self.content.cleaned_text[i:i+length]
