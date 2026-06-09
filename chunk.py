from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import re

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model
class Chunk:
    def __init__(self, text):
        self.text = text
        
    def block_split(self, max_block_words=200):
        lines = self.text.strip()
        temp_blocks = [s.strip() for s in lines.split("\n") if s.strip()]
        blocks=[]
        for block in temp_blocks:
            words = block.split() ##split bigger chunk into words
            if(len(words)>max_block_words):    #check if the word count of the chunk is greater
                ## do sentence split
                senteces = re.split(r'(?<=[.!?])\s*', block)
                curr = []
                curr_sz = 0
                for sent in senteces:
                    if(len(sent.split()) + curr_sz > max_block_words):
                        if(curr):
                            blocks.append(" ".join(curr))
                            curr = [sent]
                            curr_sz = len(sent)
                    else:
                        curr.append(sent)
                        curr_sz+=len(sent.split())
                if(curr):
                    blocks.append(" ".join(curr))            
                            
            blocks.append(block)
        return blocks
        
    def sem_chunk(self, threshold=0.42, max_words = 700, min_words= 200):
        model = get_model()
        blocks = self.block_split()
        if not blocks: return []
        embeddings = model.encode(blocks)
        chunks = []
        pre_chunk = [blocks[0]]
        pre_chunk_size = len(blocks[0].split())
        for i in range(1, len(blocks)):
            similarity = cosine_similarity([embeddings[i-1]], [embeddings[i]])[0][0]
            curr_size = len(blocks[i].split())
            if(curr_size+pre_chunk_size) > max_words:
                chunks.append(" ".join(pre_chunk))
                pre_chunk = [blocks[i]]
                pre_chunk_size = curr_size
                continue
            
            if (similarity < threshold and (curr_size+pre_chunk_size) > min_words):
                chunks.append(" ".join(pre_chunk))
                pre_chunk = [blocks[i]]
                pre_chunk_size = curr_size
            else:
                pre_chunk.append(blocks[i])
                pre_chunk_size+=curr_size
        if pre_chunk: chunks.append(" ".join(pre_chunk))
        return chunks
        
        
        