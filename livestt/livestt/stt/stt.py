from faster_whisper import WhisperModel
from typing import NamedTuple


class transcribe_return_type(NamedTuple):
    text: str
    language_probability: float
    language: str
    segment_end: float
    segment_start: float


def transcribe(
    input_file: str,
    language="en",
    model_name="tiny.en",
):
    """
    This function transcribes the given audio file and outputs the transcribed text along with other information.

    Parameters:
    input_file (str): The path to the audio file to be transcribed.
    language (str): The language of the audio file. Default is "en" (English).
    model_name (str): The name of the model to be used for transcription. Default is "tiny.en".

    Yields:
    transcribe_return_type: A named tuple containing the following fields:
        text (str): The transcribed text.
        language_probability (float): The probability of the detected language.
        language (str): The detected language.
        segment_end (float): The end time of the transcribed segment.
        segment_start (float): The start time of the transcribed segment.
    """
    model = WhisperModel(model_name, device="cpu", compute_type="int8")

    segments, info = model.transcribe(
        input_file, beam_size=5, language=language)

    for segment in segments:
        yield segment
        # return transcribe_return_type(segment.text, info.language_probability, info.language,
        # segment.end, segment.start)
    yield transcribe_return_type("", 0.0, "", 0.0, 0.0)


if __name__ == "__main__":
    text = transcribe("test.wav")
    out = ""
    for t in text:
        out += t.text
    with open("output.txt", "w+") as f:
        f.write(out)
