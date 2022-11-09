from shortuuid import uuid

from bryophyta.logic.document import Document
from bryophyta.logic.document_content import DocumentContent
from tests.utils import generate_random_string, generate_plagiarized_document

from bryophyta.logic.dropbox import Dropbox


def test_compare_2_documents():
    copied_text = generate_random_string(150)

    text_1 = generate_plagiarized_document(copied_text, 5000)
    doc_1_name = uuid()[:10]
    doc_1 = Document(1, doc_1_name, text_1)

    text_2 = generate_plagiarized_document(copied_text, 5000)
    doc_2_name = uuid()[:10]
    doc_2 = Document(2, doc_2_name, text_2)

    dropbox = Dropbox([doc_1, doc_2])
    dropbox.calculate()

    #TODO: rewrite tests after refactor
