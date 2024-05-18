from fastapi import FastAPI, File, UploadFile
from livestt.livestt import Recorder, transcribe
import threading


from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import numpy as np
import scipy.signal
import soundfile as sf
from pydub.utils import which
import requests
import numpy as np
import sounddevice as sd 



apikey = "8a887d470693e5102aa7baf862b547d5"

client = ElevenLabs(
  api_key=apikey
)

url = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


client = ElevenLabs(
  api_key=apikey, # Defaults to ELEVEN_API_KEY
)

def zombienoise(text):
  audio = client.generate(
    text=text,
    voice="Jessie",
    model="eleven_multilingual_v2"
  )
  name = "23"
  audio = client.generate(
    text=text,
    voice="Jessie",
    model="eleven_multilingual_v2"
  )
  filename = f"{name}.mp3"
  save(audio, filename)
  audio = AudioSegment.from_mp3(f"{name}.mp3")
  slowed_audio = slowDown(audio, 5)
  # slowed_audio.export(f"{filename}new.wav", format="wav")
  # slowedaudio, factor = sf.read(f"{filename}new.wav")
  # distorted_audio_data = add_dis(slowedaudio)
  # sf.write(f"{filename}zombie.wav", distorted_audio_data, factor)
  # zombieaudio = AudioSegment.from_file(f"{filename}zombie.wav")
  # audioData  = np.array(zombieaudio.get_array_of_samples())
  audioData  = np.array(slowed_audio.get_array_of_samples())
  sd.play(audioData, samplerate = audio.frame_rate)
  sd.wait()


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
  audioData  = np.array(audio.get_array_of_samples())
  sd.play(audioData, samplerate = audio.frame_rate)
  sd.wait()
  
def changep(audio, semitones):
  newRate = int(audio.frame_rate * 2**(semitones/12)) 
  newaudio = audio._spawn(audio.raw_data, overrides={'frame_rate': newRate})
  return newaudio.set_frame_rate(audio.frame_rate)

def slowDown(audio, factor):
  newaudio = audio._spawn(audio.raw_data, overrides={'frame_rate': int(audio.frame_rate*factor)})
  return newaudio.set_frame_rate(audio.frame_rate *factor)

def add_dis(audio, gain=1.5, threshold=0.5):
  newaudio = audio * gain
  newaudio[newaudio > threshold] = threshold
  newaudio[newaudio < -threshold] = -threshold
  return newaudio



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