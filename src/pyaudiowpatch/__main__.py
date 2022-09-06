from . import PyAudio

if __name__ == '__main__':
    with PyAudio() as p:
        p.print_detailed_system_info()