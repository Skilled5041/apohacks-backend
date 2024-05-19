import cohere
import sounddevice as sd
from elevenlabs import save
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment
import numpy as np


co = cohere.Client("x7vFe9vjs2kM48246X9KCg26S1IgAUBivdMF5Zwf")



apikey = "8a887d470693e5102aa7baf862b547d5"

client = ElevenLabs(
    api_key=apikey
)

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

def chat(text: str):

  stream = co.chat_stream(
    model='command-r-plus',
    preamble='''Assume you are a zombie translator, you will be give a string of letters said by a zombie, and based on this mapping 'A": "grr",
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
          " ": "hrr"' translate the string of letters of zombie noises back in to letters, based on the letters, try to make an prediction on what the zombie was trying to say. If you are unsure how to respond, just reply with a random sentence. Roleplay, meaning that you will not say anything about translating of, but JUST ONLY rely with the translated words
  ''',
    temperature=0,
    chat_history=[],
    prompt_truncation='OFF',
    message="translate '"+text+"' into english"
  )

  for event in stream:
    if event.event_type == "text-generation":
      pplnoise(event.text)
      print(event.text, end='')

