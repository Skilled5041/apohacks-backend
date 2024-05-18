import pyaudio
import wave
import threading


class Recorder:

    """
    This class is used to record audio and save it to a file.

    Attributes:
    chunk (int): The number of audio frames per buffer.
    format (int): The sample format for the recording.
    channels (int): The number of channels for the recording.
    fs (int): The sample rate of the recording.
    filename (str): The name of the output file where the recording will be saved.
    listening (bool): A flag indicating whether the recorder is currently recording.
    """

    def __init__(self, output_filename: str, chunk=1024, format=pyaudio.paInt16,
                 channels=2, samples_per_second=44100):
        
        """
        The constructor for the Recorder class.

        Parameters:
        output_filename (str): The name of the output file where the recording will be saved.
        chunk (int): The number of audio frames per buffer. Default is 1024.
        format (int): The sample format for the recording. Default is pyaudio.paInt16.
        channels (int): The number of channels for the recording. Default is 2.
        samples_per_second (int): The sample rate of the recording. Default is 44100.
        """
        
        self.chunk = chunk   # Record chunks of 1024 samples
        self.format = format
        self.channels = 2
        self.fs = samples_per_second
        self.filename = output_filename

        self.listening = False

    def _write_to_file(self):
        """
        This method writes the recorded audio to a file.
        """

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def _listen(self):
        """
        This method listens to the audio stream and records the audio frames.
        """

        while self.listening:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def start(self):

        """
        This method starts the recording process.
        """

        self.listening = True

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.fs,
            frames_per_buffer=self.chunk,
            input=True
        )

        self.frames = []

        # create thread
        self.t = threading.Thread(target=self._listen)
        self.t.start()

    def end(self):
        """
        This method ends the recording process and writes the recorded audio to a file.
        """
        self.listening = False
        self.t.join(timeout=0.1)

        self.stream.stop_stream()
        self.stream.close()

        self.p.terminate()

        self._write_to_file()


if __name__ == "__main__":
    r = Recorder("test.wav")
    import time
    r.start()
    time.sleep(3)
    r.end()
