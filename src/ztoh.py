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
    preamble='''You are a translator who translates from zombie speak to english. Make your closest estimate to the answer. Reply directly with your estimate, do not add unnecessary dialogue.
    If the input doesn't conform with the format, say "That is not zombie speech". The way english is translated to zombie speak is by replacing each letter with the following mapping, try to reverse this: 
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
  ''',
    temperature=0,
    chat_history=[],
    prompt_truncation='AUTO',
    message="The zombie text for you to translate is: "+text
  )

  for event in stream:
    if event.event_type == "text-generation":
      pplnoise(event.text)
      print(event.text, end='')

