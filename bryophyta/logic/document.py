from dataclasses import dataclass, field

from bryophyta.logic.document_content import DocumentContent, Fingerprint


@dataclass
class Match:
    document_id: int
    matching_text: str


@dataclass
class Document:
    id: int
    title: str
    content: DocumentContent
    matches: list[Match] = field(default_factory=list)
    percent_match: float = 0.0

    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.content = DocumentContent(body)

    def get_matching_text(self, fingerprint: Fingerprint) -> str:
        i = fingerprint.global_position.index
        length = self.content.k

        return self.content.cleaned_text[i:i+length]
