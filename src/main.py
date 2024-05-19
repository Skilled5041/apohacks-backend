from fastapi import FastAPI, UploadFile
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import numpy as np
import sounddevice as sd
from pedalboard import Phaser, Pedalboard, Invert, PitchShift, time_stretch
from pedalboard.io import AudioFile
from fastapi.middleware.cors import CORSMiddleware
import ztoh

from livestt.livestt import Recorder, transcribe







samplerate = 44100.0
board = Pedalboard([
    Invert(),
    Phaser(rate_hz=samplerate),
    PitchShift(semitones=-6),
])

apikey = "8a887d470693e5102aa7baf862b547d5"

client = ElevenLabs(
    api_key=apikey
)

url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

arms_raised = False
def true_arms():
    arms_raised = True

def false_arms():
    arms_raised = False





def zombienoise(text):
    audio = client.generate(
        text=text,
        voice="Jessie",
        model="eleven_multilingual_v2"
    )
    name = "24"
    filename = f"temp/{name}.mp3"
    save(audio, filename)
    audio = AudioSegment.from_mp3(f"temp/{name}.mp3")
    slowed_audio = slowDown(audio, 5)
    audioData = np.array(slowed_audio.get_array_of_samples())
    sd.play(audioData, samplerate=audio.frame_rate)
    with AudioFile(f"temp/{name}.mp3").resampled_to(samplerate) as f:
        audio = f.read(f.frames)
    effected = time_stretch(stretch_factor=0.95, input_audio=board(audio, samplerate), samplerate=samplerate)
    with AudioFile('processed-output.wav', 'w', samplerate, effected.shape[0]) as f:
        f.write(effected)
    print(effected.transpose().shape)
    sd.play(effected.transpose(), samplerate=samplerate)
    sd.wait()

def pplnoise(text):
    audio = client.generate(
        text=text,
        voice="Jessie",
        model="eleven_multilingual_v2"
    )
    name = "asdf"
    filename = f"{name}.mp3"
    save(audio, filename)
    audio = AudioSegment.from_mp3(f"{name}.mp3")
    audioData = np.array(audio.get_array_of_samples())
    sd.play(audioData, samplerate=audio.frame_rate)
    sd.wait()


def changep(audio, semitones):
    newRate = int(audio.frame_rate * 2 ** (semitones / 12))
    newaudio = audio._spawn(audio.raw_data, overrides={'frame_rate': newRate})
    return newaudio.set_frame_rate(audio.frame_rate)


def slowDown(audio, factor):
    newaudio = audio._spawn(audio.raw_data, overrides={'frame_rate': int(audio.frame_rate * factor)})
    return newaudio.set_frame_rate(audio.frame_rate * factor)


def add_dis(audio, gain=1.5, threshold=0.5):
    newaudio = audio * gain
    newaudio[newaudio > threshold] = threshold
    newaudio[newaudio < -threshold] = -threshold
    return newaudio


app = FastAPI()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)









curr_state = False

filename = "test.wav"
recorder = Recorder(filename)

def to_zombie_text(text: str) -> str:
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
        " ": " "
    }
    o = ""
    for c in text.upper():
        if c in c_map:
            o += c_map[c]
        if c not in c_map:
            o += " "
            continue
    return o


temp_count = 0

@app.post("/zombie_audio/")
async def create_upload_file(file: UploadFile):
    print(file.size)
    # Save the file in /temp
    global temp_count
    with open(f"temp/{temp_count}.ogg", "wb") as f:
        f.write(file.file.read())
    temp_count += 1
    full_text = ""
    for t in transcribe(f"temp/{temp_count - 1}.ogg"):
        print(t.text)
        full_text += t.text
    ztoh.chat(full_text)

@app.post("/upload_audio/")
async def create_upload_file(file: UploadFile):
    print(file.size)
    # Save the file in /temp


@app.post("/humanToZombie/")
async def human_to_zombie(data):
    print(data)
    zombienoise(to_zombie_text(full_text))


@app.get('/')
async def home():
    return {"Hello": "World"}


@app.get("/state/")
async def state():
    return {"state": arms_raised}


@app.get("/toggle/")
async def toggle():
    global curr_state
    curr_state = not curr_state
    return {}


@app.get("/upload/")
async def upload(text: str):
    return {"msg": "Success"}
