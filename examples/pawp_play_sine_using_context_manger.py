"""An example of how to play sounds using the 'new context manager' added to PyAudio"""

from _spinner_helper import Spinner
# Spinner is a helper class that is in the same examples folder.
# It is optional, you can safely delete the code associated with it.

import pyaudiowpatch as pyaudio
import numpy as np
import time


volume = 0.5
sample_rate = 44100
duration = 2.0
frequency = 540.0


def generate_samples(duration=duration, frequency=frequency, sample_rate=sample_rate):
    """Generate sin wave"""
    return (np.sin(2*np.pi*np.arange(sample_rate*duration)*frequency/sample_rate)).astype(np.float32)


samples = generate_samples()


def callback(in_data, frame_count, time_info, status):
    """Return data to play and PA flag"""
    return (volume*samples, pyaudio.paContinue)
    
    
if __name__ == "__main__":
    with pyaudio.PyAudio() as p, Spinner() as spinner:
        """
        Create PyAudio instance via context manager.
        Spinner is a helper class, for `pretty` output
        """
        with p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sample_rate,
                output=True,
                stream_callback=callback
        ) as stream:
            """
            Opena PA stream via context manager.
            After leaving the context, everything will
            be correctly closed(Stream, PyAudio manager)            
            """
            spinner.print(f"Playing sine wave {duration} seconds")
            time.sleep(duration) # Blocking execution while playing
