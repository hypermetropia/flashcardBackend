import requests

url ='http://127.0.0.1:8000/generate-flashcards/'
files = {'file': open("D:/2-1/2303074_DM.pdf", 'rb')}
r = requests.post(url, files=files)
print(r.json())