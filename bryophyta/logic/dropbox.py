from bryophyta.logic.document import Document, Match


class Dropbox:
    documents: list[Document]

    def __init__(self, documents: list[Document]):
        self.documents = documents

    def compare_documents(self):
        document_fingerprints = []

        for document in self.documents:
            for document_fingerprint in document.content.fingerprints:
                document_fingerprints.append((document, document_fingerprint))

        groups = {}

        for document_fingerprint in document_fingerprints:
            document, fingerprint = document_fingerprint
            try:
                groups[fingerprint.val].append(document_fingerprint)
            except KeyError:
                groups[fingerprint.val] = [document_fingerprint]

        groups = {k: v for k, v in groups.items() if len(v) > 1}

        for group in groups.values():
            for document_fingerprint in group:
                document, fingerprint = document_fingerprint
                matching_text = document.get_matching_text(fingerprint)
                yield Match(document.id, matching_text)
