from dataclasses import dataclass

from bryophyta.document import Document
from bryophyta.document_content import Fingerprint


@dataclass
class DocumentFingerprint:
    document: Document
    fingerprint: Fingerprint
        

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

        groups = {}

        for document_fingerprint in document_fingerprints:
            try:
                groups[document_fingerprint.fingerprint.val].append(document_fingerprint)
            except KeyError:
                groups[document_fingerprint.fingerprint.val] = [document_fingerprint]

        groups = {k: v for k, v in groups.items() if len(v) > 1}

        return groups # TODO: go through this and establish the relationships between documents
