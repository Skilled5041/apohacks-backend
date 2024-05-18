from transformers.pipelines.audio_utils import ffmpeg_microphone_live
from typing import Callable
from transformers import pipeline
import torch

device = "cuda:0" if torch.cuda.is_available() else "cpu"

classifier = pipeline(
    "audio-classification", model="MIT/ast-finetuned-speech-commands-v2", device=device
)


def wait(
    callback: Callable,
    args: tuple[any] | None = None,
    wake_word="sheila",
    prob_threshold=0.5,
    chunk_length_s=2.0,
    stream_chunk_s=0.25,
    debug=True,
):
    """
    This function waits for a specific wake word to be detected in the audio stream.

    Parameters:
    callback (Callable): The function to be called when the wake word is detected.
    args (tuple[any] | None): The arguments to be passed to the callback function. Default is None.
    wake_word (str): The wake word that the function is waiting for. Default is "sheila".
    prob_threshold (float): The probability threshold for the wake word detection. Default is 0.5.
    chunk_length_s (float): The length of the audio chunk to be processed at a time, in seconds. Default is 2.0.
    stream_chunk_s (float): The length of the audio stream chunk to be processed at a time, in seconds. Default is 0.25.
    debug (bool): If True, debug information will be printed. Default is True.

    Raises:
    ValueError: If the wake word is not in the set of valid class labels.

    Returns:
    None
    """
    if wake_word not in classifier.model.config.label2id.keys():
        raise ValueError(
            f"Wake word {wake_word} not in set of valid class labels, pick a wake word in the set {classifier.model.config.label2id.keys()}."
        )

    sampling_rate = classifier.feature_extractor.sampling_rate

    mic = ffmpeg_microphone_live(
        sampling_rate=sampling_rate,
        chunk_length_s=chunk_length_s,
        stream_chunk_s=stream_chunk_s,
    )

    print("Listening for wake word...")
    for prediction in classifier(mic):
        prediction = prediction[0]
        if debug:
            print(prediction)
        if prediction["label"] == wake_word:
            if prediction["score"] > prob_threshold:
                if args is not None:
                    return callback(*args)
                else:
                    return callback()


if __name__ == "__main__":
    wait(lambda x: print(x))
