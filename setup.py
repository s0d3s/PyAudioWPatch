"""PyAudio: Cross-platform audio I/O with PortAudio.

PyAudio provides Python bindings for PortAudio, the cross-platform audio I/O
library. With PyAudio, you can easily use Python to play and record audio on a
variety of platforms, such as GNU/Linux, Microsoft Windows, and Apple macOS.

PyAudio is distributed under the MIT License:

Copyright (c) 2006 Hubert Pham

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
 
import os
import sys
import logging
import platform

from setuptools import setup, Extension


__version__ = "0.2.12.7"
__author__  = "Hubert Pham(S0D3S edition)"


def get_bool_from_env(var_name, default=None):
    value = os.environ.get(var_name, default)
    return value if value is None else value.lower() in ("1", "true")


IS_CROSS_COMPILING = get_bool_from_env("PAWP_C_C_FLAG", default=None) # used when building with cibuildwheel

MAC_SYSROOT_PATH = os.environ.get("SYSROOT_PATH", None)
WIN_VCPKG_PATH = os.environ.get("VCPKG_PATH", None)
FORCE_CYGWIN_ENV = get_bool_from_env("FORCE_CYGWIN_ENV", default=None)

PORTAUDIO_PATH = os.path.abspath(os.environ.get("PORTAUDIO_PATH", "./portaudio_v19"))

VERBOSE = False
if "--pa-verbose" in sys.argv:
    VERBOSE = True
    sys.argv.remove("--pa-verbose")


def setup_extension():
    pyaudio_module_sources = ['src/_portaudiomodule.c']
    include_dirs = []
    external_libraries = ["portaudio"]
    external_libraries_path = []
    extra_compile_args = []
    extra_link_args = []
    defines = []
    
    if VERBOSE:
        extra_compile_args += ['-DVERBOSE']

    if sys.platform == 'darwin':
        # Support only dynamic linking with portaudio, since the supported path
        # is to install portaudio using a package manager (e.g., Homebrew).
        # TODO: let users pass in location of portaudio library on command line.
        defines += [('MACOSX', '1')]

        include_dirs += ['/usr/local/include', '/usr/include']
        external_libraries_path += ['/usr/local/lib', '/usr/lib']

        if MAC_SYSROOT_PATH:
            extra_compile_args += ["-isysroot", MAC_SYSROOT_PATH]
            extra_link_args += ["-isysroot", MAC_SYSROOT_PATH]
    elif sys.platform == 'win32':
        # Only supports statically linking with portaudio, since the typical
        # way users install PyAudio on win32 is through pre-compiled wheels.
        bits = platform.architecture()[0]
        if '64' in bits:
            defines.append(('MS_WIN64', '1'))
            os.environ["CC"] = "x86_64-w64-mingw32-gcc"
        else:
            os.environ["CC"] = "i686-w64-mingw32-gcc"
            extra_link_args.append("-static-libgcc")

        if WIN_VCPKG_PATH:
            include_dirs += [os.path.join(WIN_VCPKG_PATH, 'include')]
            external_libraries_path = [os.path.join(WIN_VCPKG_PATH, 'lib')]
        else:
            # If VCPKG_PATH is not set, it is likely a user oversight, as the
            # extension compiler likely won't be able to find the portaudio
            # library to link against.
            #logging.warning("Warning: VCPKG_PATH envrionment variable not set.")
            # So if VCPKG_PATH is not set, be sure to manually add the correct
            # path to portaudio's include and lib dirs, or use setuptools
            # build_ext to specify them on the command line.
            external_libraries.remove("portaudio")
            
            include_dirs += [os.path.join(PORTAUDIO_PATH, 'include')]
            
            if not IS_CROSS_COMPILING:
                extra_link_args.append(os.path.join(PORTAUDIO_PATH, 'lib/.libs/libportaudio.a'))
            elif '64' in bits:
                extra_link_args.append(os.path.join(PORTAUDIO_PATH, 'lib_dist/libportaudio-x86_64.a'))
            else:
                extra_link_args.append(os.path.join(PORTAUDIO_PATH, 'lib_dist/libportaudio-x86.a'))

        if FORCE_CYGWIN_ENV or 'ORIGINAL_PATH' in os.environ and 'cygdrive' in os.environ['ORIGINAL_PATH']:
            external_libraries += ["winmm","ole32","uuid"]
            extra_link_args += ["-lwinmm","-lole32","-luuid"]
        else:
            # The static portaudio lib does not include user32 and advapi32, so
            # those need to be linked manually.
            #external_libraries += ["user32", "Advapi32"]
            # For static linking, use MT flag to match both vcpkg's portaudio and
            # the standard portaudio cmake settings. For details, see:
            # https://devblogs.microsoft.com/cppblog/vcpkg-updates-static-linking-is-now-available/
            extra_compile_args += ["/MT"]
            external_libraries += ["winmm","ole32","uuid","advapi32","user32"]
            #extra_link_args += ["/NODEFAULTLIB:MSVCRT"]
    else:
        # GNU/Linux and other posix-like OSes will dynamically link to
        # portaudio, installed by the package manager.
        include_dirs += ['/usr/local/include', '/usr/include']
        external_libraries_path += ['/usr/local/lib', '/usr/lib']

    return Extension(
        '_portaudiowpatch',
        sources=pyaudio_module_sources,
        include_dirs=include_dirs,
        define_macros=defines,
        libraries=external_libraries,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        library_dirs=external_libraries_path)


with open('README.md', 'r', encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='PyAudioWPatch',
    version=__version__,
    author=__author__,
    url="https://github.com/s0d3s/PyAudioWPatch/",
    description="PortAudio fork with WASAPI loopback support",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="Apache-2.0 license",
    packages=["pyaudiowpatch"],
    package_dir={"": "src"},
    scripts=[],
    extras_require={
        "test": ["numpy"],
    },
    ext_modules=[setup_extension()],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Sound/Audio"
    ])
