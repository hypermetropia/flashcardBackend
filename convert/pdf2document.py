from unstructured.partition.auto import partition

class PDF2Document:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def convert(self):
        doc = partition(filename=self.pdf_path, strategy='auto')
        text = "\n".join([str(i) for i in doc])
        return text
        