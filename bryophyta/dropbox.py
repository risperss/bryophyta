from dataclasses import dataclass

from bryophyta.document import Document
from bryophyta.document_content import Fingerprint


class DocumentFingerprint:
    document: Document
    fingerprint: Fingerprint

    @property
    def val(self):
        return self.fingerprint.val

    def __eq__(self, other):
        if isinstance(other, DocumentFingerprint):
            return self.val == other.val
        raise NotImplementedError

    def __lt__(self, other):
        if isinstance(other, DocumentFingerprint):
            return self.val < other.val
        raise NotImplementedError


class Match:
    f1: DocumentFingerprint    
    f2: DocumentFingerprint
    matching_text: str # TODO: find proper home


@dataclass
class DocumentReport:
    document: Document
    matches: list[Match]
    percent_match: float


@dataclass
class DropboxReport:
    document_reports: list[DocumentReport]


class Dropbox:
    documents: list[Document]

    def __init__(self, documents: list[Document]):
        self.documents = documents

    def generate_report(self) -> DropboxReport:
        document_fingerprints: list[DocumentFingerprint] = []

        for document in self.documents:
            for document_fingerprint in document.content.fingerprints:
                document_fingerprints.append(DocumentFingerprint(document, document_fingerprint))

        document_fingerprints.sort()

        groups: dict[int, list[DocumentFingerprint]] = {}

        for document_fingerprint in document_fingerprints:
            try:
                groups[document_fingerprint.val].append(document_fingerprint)
            except KeyError:
                groups[document_fingerprint.val] = [document_fingerprint]

        return groups # TODO: go through this and establish the relationships between documents
