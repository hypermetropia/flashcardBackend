from convert.pdf2document import PDF2Document
from chunk import Chunk
from flashcard import FlashCard
class Pipline:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
    def pipline(self):
        converter = PDF2Document(self.pdf_path)
        text = converter.convert()
        chunk = Chunk(text)
        chunks = chunk.sem_chunk()
        # print(chunks[0]);
        cards = []
        for i in chunks:
            flashcard = FlashCard()
            curr_cards = flashcard.gen(i)
            if(len(curr_cards)):
                cards.append(curr_cards[0])
        print(len(cards))
        return cards
        
        
        