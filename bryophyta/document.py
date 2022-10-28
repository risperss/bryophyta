from dataclasses import dataclass

from bryophyta.document_content import DocumentContent


@dataclass
class Author:
    name: str


@dataclass
class Document():
    name: str
    author: Author
    content: DocumentContent
