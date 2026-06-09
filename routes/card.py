from fastapi import FastAPI, UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
import shutil
import os
from pipline import Pipline
from model.FlashCard import insert_table, get_table, delete_table

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/generate-flashcards/")
async def generate_flashcards(collection, file: UploadFile = File(...)):
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        if(not os.path.exists(file_path)):
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        # Run your pipeline
        pipeline = Pipline(pdf_path=file_path)
        result = pipeline.pipline()
        print(result)
        insert_table(collection, result)

@router.get("/collections/{collection_name}")
async def get_collection(collection_name: str):
    result = await get_table(collection_name)
    return result             

@router.delete("/delete/{id}")
async def delete_flashcard(collection_name: str):
    await delete_table(id=id)
    return {"message":f"{id} deleted succesfully"} 
    
