from fastapi import FastAPI, File, UploadFile
import threading
import random
from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import numpy as np
import sounddevice as sd
from gtts import gTTS
from pedalboard import Phaser, Pedalboard, Invert, PitchShift, time_stretch
from pedalboard.io import AudioFile

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
    effected = time_stretch(stretch_factor=0.95, input_audio=board(audio, samplerate), samplerate=samplerate)
    with AudioFile('processed-output.wav', 'w', samplerate, effected.shape[0]) as f:
        f.write(effected)
    print(effected.transpose().shape)
    sd.play(effected.transpose(), samplerate=samplerate)
    sd.wait()


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
    return newstr

def pplnoise(text):
    audio = client.generate(
        text=text,
        voice="Jessie",
        model="eleven_multilingual_v2"
    )
    name = input("Enter the name of the file: ")
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

curr_state = False

filename = "test.wav"
recorder = Recorder(filename)


@app.post("/upload_audio/")
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

    zombienoise(to_zombie_text(full_text))


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
