# livestt

## Installation

```
pip install livestt # this could take a while
````

## Usage
Livestt gives access to 3 main classes/functions. 

### Wait for the wake word
```python
from livestt import wait

def callback_func():
    print("Wakeword said!")

wait(callback=callback_func)
```

The `wait` function takes in these args:

`callback` (Callable): The function to be called when the wake word is detected.

`args` (tuple[any] | None): The arguments to be passed to the callback function. The default is None.

`wake_word` (str): The wake word that the function is waiting for. The default is "Sheila".

`prob_threshold` (float): The probability threshold for the wake word detection. The default is 0.5.

`chunk_length_s` (float): The length of the audio chunk to be processed at a time, in seconds. The default is 2.0.

`stream_chunk_s` (float): The length of the audio stream chunk to be processed at a time, in seconds. The default is 0.25.

`debug` (bool): If True, debug information will be printed. The default is True.

Raises:
`ValueError`: If the wake word is not in the set of valid class labels.

Returns:
`None`

### Record audio
```python
from livestt import Recorder
import time

recorder = Recorder("test.wav")

recorder.start()    # Starts recorder thread
time.sleep(5)   # Waits before ending thread
recorder.end()  # Writes recording to "test.wav"
```


The `Recorder` class when started starts a new recorder thread where it will listen to the audio until the thread is ended. Upon the thread ending, the recording will be saved to a file. The `Recorder` class takes these args:

`chunk` (int): The number of audio frames per buffer.

`format` (int): The sample format for the recording.

`channels` (int): The number of channels for the recording.

`fs` (int): The sample rate of the recording.

`filename` (str): The name of the output file where the recording will be saved. **The file_ MUST currently be .wav**

`listening` (bool): A flag indicating whether the recorder is currently recording.

### Transcribe a given audio file
```python 
from livestt import transcribe

transcription = transcribe("test.wav")

for t in transcription:
    print(t.text)

```

The `transcribe` function transcribes the given audio file and outputs the transcribed text along with other information. The `transcribe` function takes these args:

`input_file` (str): The path to the audio file to be transcribed.

`language` (str): The language of the audio file. The default is "en" (English).

`model_name` (str): The name of the model to be used for transcription. The default is "tiny.en".

This function yields a tuple with the following fields:


`text` (str): The transcribed text.

`language_probability` (float): The probability of the detected language.

`language` (str): The detected language.

`segment_end` (float): The end time of the transcribed segment.

`segment_start` (float): The start time of the transcribed segment.

## Examples
For a full example, check out the example in the file `example/main.py`.

## Tech stack

- [Pyaudio](https://people.csail.mit.edu/hubert/pyaudio/) for recording audio.
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) for transcription.
- [openWakeWord](https://huggingface.co/spaces/davidscripka/openWakeWord) for wakeword detection.

## Acknowledgments
Thanks to [Kolja](https://github.com/KoljaB) for the inspiration. I couldn't figure out how to use his library so I made my own. Check this out [here](https://github.com/KoljaB/RealtimeSTT).

## Contribution
Contributions are always welcome! Open an issue or make a PR. Or just contact me on discord: @a3l6

## Author(s)
- [@a3l6](https://www.github.com/a3l6)