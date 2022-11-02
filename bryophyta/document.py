from dataclasses import dataclass

from bryophyta.document_content import DocumentContent, Fingerprint


@dataclass
class Author:
    name: str


@dataclass
class Document():
    name: str
    author: Author
    content: DocumentContent
