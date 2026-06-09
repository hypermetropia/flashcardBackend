from ollama import generate
from json import loads
import json
import re
class FlashCard:
    def __init__(self): pass
    def parse_json(self,text):
        arrays = re.findall(r'\[.*?\]', text, re.DOTALL)
        result = []
        for arr in arrays:
            try:
                result.append(loads(arr))
            except json.JSONDecodeError:
                pass

        return result
    def gen(self, chunk):
        prompt = """
        You are an expert educator. And given content. Now,
        Generate 4 flash cards
        Format:
        [
        {
            "q": "...",
            "a": "..."
        }
        ]
        Rules:
            - Each flashcard must be concise and focused on one idea
            - Use simple, clear language
            - Avoid ambiguity
            - Include definitions, key facts,  important concepts. Also the questions whose answer will be 200 to 500 words
            - Prefer question-answer format
            - Also include questions with the words explain, eleborate(with bigger answers)
            - You MUST output ONLY valid JSON.
                No explanations.
                No markdown.
                No code block.
                No extra text before or after.
                If you output invalid JSON, it will be rejected. Be extremely strict.
                Ensure output is strictly parsable by json.loads() in Python.
                Your output must start with '[' and end with ']'.
                There must be exactly one JSON array. Otherwise it will be rejected. Be extremely strict.
        the content:
        
        """+chunk

        
        no_of_try = 0
        while(True):
            try:    
                no_of_try+=1
                response = generate(model="llama3.2", prompt=prompt)
                result = response.response
                result = self.parse_json(result)[0]
                if(no_of_try>10):
                    no_of_try = 0
                    return []
                return result
            except:
                continue
        