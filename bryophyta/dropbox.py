from dataclasses import dataclass

from bryophyta.document import Document
from bryophyta.document_content import Fingerprint


class DocumentFingerprint:
    document: Document
    fingerprint: Fingerprint


class Match:
    document_fingerprint_1: DocumentFingerprint    
    document_fingerprint_1: DocumentFingerprint
    matching_text: str


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

    def generate_report(self):
        return self.compare_documents()

    def compare_documents(self):
        report = DropboxReport

        n = len(self.documents)
        for i in range(n - 1):
            document = self.documents[i]
            for j in range(i + 1, n):
                self.compare_documents(document, self.documents[j])

    def compare_documents(self, document_1: Document, document_2: Document, report: DropboxReport):
        for fingerprint in document_1.content.fingerprints:
            if fingerprint in document_2.content.fingerprints:
                pass
