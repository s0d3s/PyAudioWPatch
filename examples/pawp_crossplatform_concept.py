"""
    PyAudioWPatch can be compiled for other operating systems,
    but for now it is planned to support precompiled packages only for Windows

    So if you want to keep it cross-platform, we can use PyAudioWPatch only
    for Windows and original PyAudio for other systems
    
    So you can do something like this:
"""

import sys

if sys.platform.startswith("win"):
    import pyaudiowpatch as pyaudio
else:
    import pyaudio

if __name__ == '__main__':
    print('This is just a concept, not a working example.\nPlease read the comments.')