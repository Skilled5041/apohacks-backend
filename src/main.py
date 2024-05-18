from fastapi import FastAPI, File, UploadFile
from livestt.livestt import Recorder, transcribe
import threading

app = FastAPI()

curr_state = False

filename = "test.wav"
recorder = Recorder(filename)


def ModdedCeaserCipher(text: str) -> str:
    c_map = {
        "A": "grr",
        "B": "argh",
        "C": "ugh",
        "D": "rawr",
        "E": "brr",
        "F": "gah",
        "G": "urr",
        "H": "blur",
        "I": "hmm",
        "J": "zzz",
        "K": "rarr",
        "L": "blargh",
        "M": "snar",
        "N": "arg",
        "O": "mur",
        "P": "grar",
        "Q": "urgh",
        "R": "blurr",
        "S": "snarl",
        "T": "garr",
        "U": "hur",
        "V": "braar",
        "W": "snur",
        "X": "grargh",
        "Y": "grur",
        "Z": "arrgh",
        " ": "hrr"
    }
    o = ""
    for c in text:
        if c.upper() in c_map:
            o += c_map[c.upper()]
            continue
        o += " "
    return o


def listener():
    started = False
    while True:
        # print(curr_state, started)
        if curr_state and not started:
            recorder.start()
            started = True
        elif not curr_state and started:
            recorder.end()
            started = False
            text = list(transcribe(filename))[0]
            print(ModdedCeaserCipher(text.text))


thread = threading.Thread(target=listener)
thread.start()

temp_count = 0


@app.post("/upload_audio/")
async def create_upload_file(file: UploadFile):
    print(file.size)
    # Save the file in /temp
    global temp_count
    with open(f"temp/{temp_count}.ogg", "wb") as f:
        f.write(file.file.read())
    temp_count += 1
    for t in transcribe(f"temp/{temp_count - 1}.ogg"):
        print(t.text)


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
