from fastapi import FastAPI, UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
import shutil
import os
from pipline import Pipline
from model.FlashCard import insert_table, get_table, delete_table
import asyncio
router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/generate-flashcards/")
async def generate_flashcards(collection:str, file: UploadFile = File(...)):
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        if(not os.path.exists(file_path)):
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        pipeline = Pipline(pdf_path=file_path)
        try:
            result = await asyncio.to_thread(pipeline.pipline)
        finally:
            os.remove(file_path)
        await insert_table(collection, result)
        return JSONResponse({"message": "created", "count": len(result)}, status_code=201)

@router.get("/collections/{collection_name}")
async def get_collection(collection_name: str):
    result = await get_table(collection_name)
    return result             

@router.delete("/delete/{id}")
async def delete_flashcard(id: int):
    await delete_table(id=id)
    return {"message":f"{id} deleted succesfully"} 
    
