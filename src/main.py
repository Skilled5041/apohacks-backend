from fastapi import FastAPI, File, UploadFile
from livestt import transcribe

app = FastAPI()

@app.get('/')
async def home():
    return {"Hello": "World"}

@app.get("/upload/")
async def uploadtext: str):
    return {"msg": "Success"}