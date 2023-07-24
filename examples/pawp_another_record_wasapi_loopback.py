"""A simple example of recording from speakers ('What you hear') using the WASAPI loopback device

Functionality is similar to `pawp_record_wasapi_loopback`, but made in another way:
 - new methods of improving life are used
 - Instead of `callback`, "step-by-step recording" is used
"""

from _spinner_helper import Spinner
# Spinner is a helper class that is in the same examples folder.
# It is optional, you can safely delete the code associated with it.

import pyaudiowpatch as pyaudio
import wave

duration = 5.0
data_format = pyaudio.paInt16

filename = "loopback_record.wav"
    
    
if __name__ == "__main__":
    with pyaudio.PyAudio() as p, Spinner() as spinner:
        """
        Create PyAudio instance via context manager.
        Spinner is a helper class, for `pretty` output
        """

        try:
            # Get loopback of default WASAPI speaker
            default_speakers = p.get_default_wasapi_loopback()

        except OSError:
            spinner.print("Looks like WASAPI is not available on the system. Exiting...")
            spinner.stop()
            exit()

        except LookupError:
            spinner.print("Default loopback output device not found.\n\nRun `python -m pyaudiowpatch` to check available devices.\nExiting...\n")
            spinner.stop()
            exit()

        RATE = int(default_speakers["defaultSampleRate"])
        SAMPLE_SIZE = p.get_sample_size(data_format)

        spinner.print(f"Recording from: ({default_speakers['index']}){default_speakers['name']}")
        
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(default_speakers["maxInputChannels"])
        wave_file.setsampwidth(SAMPLE_SIZE)
        wave_file.setframerate(RATE)

        with p.open(
                format=data_format,
                channels=default_speakers["maxInputChannels"],
                rate=RATE,
                input=True,
                input_device_index=default_speakers["index"],
        ) as stream:
            """
            Opena PA stream via context manager.
            After leaving the context, everything will
            be correctly closed(Stream, PyAudio manager)            
            """
            spinner.print(f"The next {duration} seconds will be written to {filename}")

            for i in range(0, int(RATE / SAMPLE_SIZE * duration)):
                """Record audio step-by-step"""
                data = stream.read(SAMPLE_SIZE)
                wave_file.writeframes(data)
        
        wave_file.close()
