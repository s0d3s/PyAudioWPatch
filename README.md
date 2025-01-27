<div align="center">

<!---![PyAudioWasapiLoopbackPatch](assets/snake-350_patch.png)-->
<img alt="PyAudio Wasapi Loopback Patch" src="https://raw.githubusercontent.com/s0d3s/PyAudioWPatch/media_content_distribution/assets/snake_trace_clear.svg" height="414"/>

# PyAudioWPatch

This fork will allow you to use the WASAPI device as loopback using **PyAudio**.
<br>
So you can *use speakers to record audio* ✨


![Last Commit](https://img.shields.io/github/last-commit/s0d3s/PyAudioWPatch)
[![Wheels](https://img.shields.io/pypi/wheel/PyAudioWpatch)](https://pypi.org/project/PyAudioWPatch/)
![Downloads](https://img.shields.io/pypi/dm/PyAudioWPatch)
![Py Version](https://img.shields.io/pypi/pyversions/PyAudioWpatch)
[![Latest release](https://img.shields.io/github/v/release/s0d3s/PyAudioWPatch)](https://github.com/s0d3s/PyAudioWPatch/releases/latest)

</div>

<br /><br />

## For whom?

If you want to record sound from speakers in python, then this fork is for you. You can get recording from any device that supports WASAPI, for example, you can even record audio from *Bluetooth* headphones🎧

> PyAudioW(*indows|ASAPI*)Patch come only with WMME, DirectX and WASAPI support
> if you need more -> create an issue

## How

The Windows Audio Session API ([WASAPI](https://docs.microsoft.com/en-us/windows/win32/coreaudio/wasapi)) allows you to use output devices (that support this API) in loopback mode. At the time of release, it was impossible to achieve this using the original version of PyAudio.

> Note: Now WASAPI loopback devices are duplicated at the end of the list as virtual devices. That is, to record from speakers, you need to use not just a WASAPI device, but its loopback analogue. All loopback devices are **input devices**.

## How to use

*Read -> Install -> Enjoy!* ↣ *Press ⭐*

### Installation

```bash
pip install PyAudioWPatch
```
> Wheels are available for **Windows**, Python *3.{7,8,9,10,11,12,13}*.<br />
> All wheels support APIs: WMME, WASAPI, DirectX(DSound).

### In code

With new features:

```python
import pyaudiowpatch as pyaudio

with pyaudio.PyAudio() as p:
    # Open PyA manager via context manager
    with p.open(...) as stream:
        # Open audio stream via context manager
        # Do some stuff
        ...
```

Or in original PyAudio way:

```python
import pyaudiowpatch as pyaudio

p = pyaudio.PyAudio()
stream = p.open(...)

# Do some stuff
...

stream.stop_stream()
stream.close()

# close PyAudio
p.terminate()
```

### Difference with PyAudio

 - The behavior of all standard methods is unchanged
 - Added several *life-improving* methods
 - Fixed problem with name encoding
 - Ability to record audio from WASAPI loopback devices (see [example](https://github.com/s0d3s/PyAudioWPatch/blob/master/examples/pawp_record_wasapi_loopback.py))
 
#### More detailed
 - new methods:
   - [`get_host_api_info_generator`](https://github.com/s0d3s/PyAudioWPatch/blob/master/src/pyaudiowpatch/__init__.py#L1082) - Iterate over all Host APIs
   - [`get_device_info_generator`](https://github.com/s0d3s/PyAudioWPatch/blob/master/src/pyaudiowpatch/__init__.py#L1096) - Iterate over all devices
   - [`get_device_info_generator_by_host_api`](https://github.com/s0d3s/PyAudioWPatch/blob/master/src/pyaudiowpatch/__init__.py#L1109) - Iterate over all devices, by specific Host API(index/type)
   - [`get_loopback_device_info_generator`](https://github.com/s0d3s/PyAudioWPatch/blob/master/src/pyaudiowpatch/__init__.py#L1133) - Iterate over all devices(with loopback mode)
   - [`print_detailed_system_info`](https://github.com/s0d3s/PyAudioWPatch/blob/master/src/pyaudiowpatch/__init__.py#L1149) - Print some info about Host Api and devices
   - [`get_default_wasapi_loopback`](https://github.com/s0d3s/PyAudioWPatch/blob/master/src/pyaudiowpatch/__init__.py#L1255) - Return `loopback` for default speakers
   - [`get_wasapi_loopback_analogue_by_index`](https://github.com/s0d3s/PyAudioWPatch/blob/master/src/pyaudiowpatch/__init__.py#L1243) - Return `loopback` for device via index
   - [`get_wasapi_loopback_analogue_by_dict`](https://github.com/s0d3s/PyAudioWPatch/blob/master/src/pyaudiowpatch/__init__.py#L1213) - Return `loopback` for device related to `info_dict`
   - [`get_default_wasapi_device`](https://github.com/s0d3s/PyAudioWPatch/blob/master/src/pyaudiowpatch/__init__.py#L1191) - Return default (out/in)put device for `WASAPI` driver

 - new features:
   - Context manager support, for PyAudio(manager) and Stream classes
   - Run `python -m pyaudiowpatch` to get list of devices(like `print_detailed_system_info` call)
 
#### Examples:
 - 🆕 [Sequential recording from speakers](https://github.com/s0d3s/PyAudioWPatch/blob/master/examples/pawp_another_record_wasapi_loopback.py)
 - [Play sine, using \'new context manager'](https://github.com/s0d3s/PyAudioWPatch/blob/master/examples/pawp_play_sine_using_context_manger.py)
 - [Record audio from default speakers](https://github.com/s0d3s/PyAudioWPatch/blob/master/examples/pawp_record_wasapi_loopback.py)
 - [Simple recording app](https://github.com/s0d3s/PyAudioWPatch/blob/master/examples/pawp_simple_recording_app.py)
 - [Cross-platform concept (Not example)](https://github.com/s0d3s/PyAudioWPatch/blob/master/examples/pawp_crossplatform_concept.py)
<!---
 - [Play sine, using \'new context manager'](examples/pawp_play_sine_using_context_manger.py)
 - [Record from audio from default speakers](examples/pawp_record_wasapi_loopback.py)
 - [Cross-platform concept (Not example)](examples/pawp_crossplatform_concept.py)-->
 
## Sources

The following were taken as a basis:

 - PortAudio v19 \[[8b6d16f26ad660e68a97743842ac29b939f3c0c1](https://github.com/PortAudio/portaudio/commit/8b6d16f26ad660e68a97743842ac29b939f3c0c1)]
 - PyAudio v0.2.12
 
## How to build manually

 - Build PortAudio (using the instructions in the [README](portaudio_v19/README.md))
 - ~~Install [~~python~~](https://www.python.org/downloads/)~~
 - run in the PyAudioWPatch directory:
   ```bush
   python setup.py install
   ```
 - ???
 - Profit.
 
 Also you can build wheel**s**:
 - `pip install cibuildwheel`
 - Run in Cygwin:
    ```bash
    ./cygwin_cibuildwheel_build.sh
    ```
 - Get your wheels in the `./wheelhouse` folder

---

<div align="center">

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=s0d3s/PyAudioWPatch&type=Date)](https://star-history.com/#s0d3s/PyAudioWPatch&Date)

## Origin README

</div>

<img align="right" width="200" style="margin-left: 3px" src="https://people.csail.mit.edu/hubert/pyaudio/images/snake-300.png">

## PyAudio

PyAudio provides Python bindings for PortAudio v19, the cross-platform audio I/O library. With PyAudio, you can easily use Python to play and record audio on a variety of platforms, such as GNU/Linux, Microsoft Windows, and Apple macOS.

PyAudio is distributed under the MIT License.

* [Homepage](https://people.csail.mit.edu/hubert/pyaudio/)
* [API Documentation](https://people.csail.mit.edu/hubert/pyaudio/docs/)
* [PyPi](https://pypi.python.org/pypi/PyAudio)

## Installation

See the INSTALLATION file in the source distribution for details. In summary, install PyAudio using `pip` on most platforms.

### Windows

```sh
python -m pip install pyaudio
```

This installs the precompiled PyAudio library with PortAudio v19 19.7.0 included. The library is compiled with support for Windows MME API, DirectSound, WASAPI, and WDM-KS. It does not include support for ASIO. If you require support for APIs not included, you will need to compile PortAudio and PyAudio.

### macOS

Use [Homebrew](https://brew.sh) to install the prerequisite [portaudio](http://portaudio.com) library, then install PyAudio using `pip`:

```sh
brew install portaudio
pip install pyaudio
```

### GNU/Linux

Use the package manager to install PyAudio. For example, on Debian-based systems:

```sh
sudo apt install python3-pyaudio
```

Alternatively, if the latest version of PyAudio is not available, install it using `pip`. Be sure to first install development libraries for `portaudio19` and `python3`.

### Building from source

See the INSTALLATION file.

## Documentation & Usage Examples

* Read the [API Documentation](https://people.csail.mit.edu/hubert/pyaudio/docs/), or generate it from the source using [`sphinx`](https://www.sphinx-doc.org/).

* Usage examples are in the `examples` directory of the source distribution, or see the [project homepage](https://people.csail.mit.edu/hubert/pyaudio/).

## License

PyAudio is distributed under the MIT License. See LICENSE.txt.
