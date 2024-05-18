from fastapi import FastAPI, File, UploadFile
import livestt

app = FastAPI()

curr_state = False


@app.get('/')
async def home():
    return {"Hello": "World"}

@app.get("/state/")
async def state():
    return {"state": curr_state}

@app.get("/toggle/")
async def toggle():
    global curr_state
    curr_state = not curr_state
    return {}

@app.get("/upload/")
async def upload(text: str):
    return {"msg": "Success"}