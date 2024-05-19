from fastapi import FastAPI, UploadFile
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import numpy as np
import sounddevice as sd
from pedalboard import Phaser, Pedalboard, Invert, PitchShift, time_stretch
from pedalboard.io import AudioFile
from fastapi.middleware.cors import CORSMiddleware

import src.ztoh
from livestt.livestt import transcribe
from src import ztoh

samplerate = 44100.0
board = Pedalboard([
    Invert(),
    PitchShift(semitones=-6),
    Phaser(rate_hz=samplerate),
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
    with AudioFile(f"temp/{name}.mp3").resampled_to(samplerate) as f:
        audio = f.read(f.frames)
    effected = time_stretch(stretch_factor=0.90, input_audio=board(audio, samplerate), samplerate=samplerate)
    with AudioFile('processed-output.wav', 'w', samplerate, effected.shape[0]) as f:
        f.write(effected)
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
c_map = {
    "A": "grr",
    "B": "argh",
    "C": "ugh",
    "D": "rawr",
    "E": " ",
    "F": "gah",
    "G": "urr",
    "H": " ",
    "I": "hmm",
    "J": " ",
    "K": "rarr",
    "L": "blargh",
    "M": "snar",
    "N": "arg",
    "O": "mur",
    "P": "grar",
    "Q": "urgh",
    "R": "rrurr",
    "S": "uarr",
    "T": "garr",
    "U": "hur",
    "V": "braar",
    "W": "snur",
    "X": "grargh",
    "Y": " ",
    "Z": " ",
    " ": " "
}


def to_zombie_text(text: str) -> str:
    newstr = ""
    for c in text.upper():
        if c_map.get(c) is not None:
            newstr += c_map.get(c)
    print(newstr)
    return newstr.strip()


temp_count = 0


@app.post("/zombie_audio/{transcript}")
async def create_upload_file(transcript: str):
    transcript = transcript.replace("%20", " ")
    zombie_text = to_zombie_text(transcript)
    ztoh.chat(zombie_text)


@app.post("/upload_audio/")
async def create_upload_file(file: UploadFile):
    print(file.size)
    # Save the file in /temp


@app.post("/humanToZombie/{transcript}")
async def human_to_zombie(transcript: str):
    transcript = transcript.replace("%20", " ")
    print(transcript)
    zombienoise(to_zombie_text(transcript))
    return {}


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
