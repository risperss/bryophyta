import random
import string
import unittest
from shortuuid import uuid

import lorem
from bryophyta.document import Author, Document
from bryophyta.document_content import DocumentContent

from bryophyta.dropbox import Dropbox


class Test(unittest.TestCase):
    def test_generate_report(self):
        copied_text = lorem.paragraph()

        text_1 = generate_doc_text(copied_text=copied_text)
        author_1 = Author("Adam")
        doc_1_name = uuid()[:10]
        doc_1 = Document(doc_1_name, author_1, DocumentContent(text_1))

        text_2 = generate_doc_text(copied_text=copied_text)
        author_2 = Author("Thomas")
        doc_2_name = "Disco Irish"
        doc_2 = Document(doc_2_name, author_2, DocumentContent(text_2))

        documents = [doc_1, doc_2]

        dropbox = Dropbox(documents)

        report = dropbox.generate_report()

        import pdb; pdb.set_trace()

def generate_doc_text(
    copied_text: str = None, 
    num_words: int = 5000, 
) -> str:
    copied_text = copied_text or lorem.paragraph()
    num_chars = 5 * num_words

    index = random.randint(0, num_chars)
    letters = string.ascii_lowercase
    
    text = [random.choice(letters) for _ in range(num_chars)]
    text.insert(index, copied_text)
    text = "".join(text)

    return text
