import unittest
from shortuuid import uuid

from bryophyta.document import Author, Document
from bryophyta.document_content import DocumentContent
from tests.utils import generate_random_string, generate_plagiarized_document

from bryophyta.dropbox import Dropbox


class TestDropbox(unittest.TestCase):
    def test_generate_report(self):
        copied_text = generate_random_string(150)

        text_1 = generate_plagiarized_document(copied_text, 5000)
        author_1 = Author("Adam")
        doc_1_name = uuid()[:10]
        doc_1 = Document(doc_1_name, author_1, DocumentContent(text_1))

        text_2 = generate_plagiarized_document(copied_text, 5000)
        author_2 = Author("Thomas")
        doc_2_name = uuid()[:10]
        doc_2 = Document(doc_2_name, author_2, DocumentContent(text_2))

        documents = [doc_1, doc_2]

        dropbox = Dropbox(documents)

        report = dropbox.generate_report()

        import pdb; pdb.set_trace()
