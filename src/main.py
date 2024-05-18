from fastapi import FastAPI, File, UploadFile
from livestt.livestt import Recorder, transcribe
import threading


app = FastAPI()

curr_state = False

filename = "test.wav"
recorder = Recorder(filename)


def ModdedCeaserCipher(text: str, shift: int) -> str:
    allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    o = ""
    for c in text:
        if c not in allowed:
            o += " "
            continue




def listener():
    started = False
    while True:
        #print(curr_state, started)
        if curr_state and not started:
            recorder.start()
            started = True
        elif not curr_state and started:
            recorder.end()
            started = False
            for t in transcribe(filename):
                print(t.text)


thread = threading.Thread(target=listener)
thread.start()


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