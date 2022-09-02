import os
import sys
import time
import unittest

import pyaudio

# To skip tests requiring hardware, set this environment variable:
SKIP_HW_TESTS = 'PYAUDIO_SKIP_HW_TESTS' in os.environ

class PyAudioErrorTests(unittest.TestCase):
    def setUp(self):
        self.p = pyaudio.PyAudio()

    def tearDown(self):
        self.p.terminate()

    def test_invalid_sample_size(self):
        with self.assertRaises(ValueError) as cm:
            self.p.get_sample_size(10)
        e = cm.exception
        self.assertEqual(e.args[1], pyaudio.paSampleFormatNotSupported)

    def test_invalid_width(self):
        with self.assertRaises(ValueError):
            self.p.get_format_from_width(8)

    def test_invalid_hostapi_type(self):
        with self.assertRaises(IOError) as cm:
            self.p.get_host_api_info_by_type(-1)
        e = cm.exception
        self.assertEqual(e.args[0], pyaudio.paHostApiNotFound)

    def test_invalid_hostapi_index(self):
        with self.assertRaises(IOError) as cm:
            self.p.get_host_api_info_by_index(-1)
        e = cm.exception
        self.assertEqual(e.args[0], pyaudio.paInvalidHostApi)

    def test_valid_host_api_invalid_devinfo(self):
        with self.assertRaises(IOError) as cm:
            self.p.get_device_info_by_host_api_device_index(0, -1)
        e = cm.exception
        self.assertTrue(e.args[0] in (pyaudio.paInvalidDevice,
                                      pyaudio.paInvalidHostApi))

    def test_invalid_host_api_valid_devinfo(self):
        with self.assertRaises(IOError) as cm:
            self.p.get_device_info_by_host_api_device_index(-1, 0)
        e = cm.exception
        self.assertTrue(e.args[0] in (pyaudio.paInvalidDevice,
                                      pyaudio.paInvalidHostApi))

    def test_invalid_device_devinfo(self):
        with self.assertRaises(IOError) as cm:
            self.p.get_device_info_by_index(-1)
        e = cm.exception
        self.assertEqual(e.args[0], pyaudio.paInvalidDevice)

    @unittest.skipIf(SKIP_HW_TESTS, 'audio hardware required.')
    def test_error_without_stream_start(self):
        with self.assertRaises(IOError) as cm:
            stream = self.p.open(channels=1,
                                 rate=44100,
                                 format=pyaudio.paInt16,
                                 input=True,
                                 start=False)  # not starting stream
            stream.read(2)

        e = cm.exception
        self.assertEqual(e.args[0], pyaudio.paStreamIsStopped)

    @unittest.skipIf(SKIP_HW_TESTS, 'audio hardware required.')
    def test_error_writing_to_readonly_stream(self):
        with self.assertRaises(IOError) as cm:
            stream = self.p.open(channels=1,
                                 rate=44100,
                                 format=pyaudio.paInt16,
                                 input=True)
            stream.write('foo')

        e = cm.exception
        self.assertEqual(e.args[1], pyaudio.paCanNotWriteToAnInputOnlyStream)

    @unittest.skipIf(SKIP_HW_TESTS, 'audio hardware required.')
    def test_error_negative_frames(self):
        with self.assertRaises(ValueError):
            stream = self.p.open(channels=1,
                                 rate=44100,
                                 format=pyaudio.paInt16,
                                 input=True)
            stream.read(-1)

    @unittest.skipIf(SKIP_HW_TESTS, 'audio hardware required.')
    def test_invalid_attr_on_closed_stream(self):
        stream = self.p.open(channels=1,
                             rate=44100,
                             format=pyaudio.paInt16,
                             input=True)
        stream.close()
        with self.assertRaises(IOError) as cm:
            stream.get_input_latency()
        e = cm.exception
        self.assertEqual(e.args[0], pyaudio.paBadStreamPtr)

        with self.assertRaises(IOError) as cm:
            stream.read(1)
        e = cm.exception
        self.assertEqual(e.args[0], pyaudio.paBadStreamPtr)

    def test_invalid_format_supported(self):
        with self.assertRaises(ValueError) as cm:
            self.p.is_format_supported(8000, -1, 1, pyaudio.paInt16)
        e = cm.exception
        self.assertEqual(e.args[1], pyaudio.paInvalidDevice)

        with self.assertRaises(ValueError) as cm:
            self.p.is_format_supported(8000, 0, -1, pyaudio.paInt16)
        e = cm.exception
        self.assertEqual(e.args[1], pyaudio.paInvalidChannelCount)

    # It's difficult to invoke an underflow on ALSA, so skip.
    @unittest.skipIf('linux' in sys.platform,
                     'skipping underflow test on linux.')
    @unittest.skipIf(SKIP_HW_TESTS, 'audio hardware required.')
    def test_write_underflow_exception(self):
        stream = self.p.open(channels=1,
                             rate=44100,
                             format=pyaudio.paInt16,
                             output=True)
        time.sleep(0.5)
        stream.write('\x00\x00\x00\x00', exception_on_underflow=False)

        with self.assertRaises(IOError) as err:
            # The sleep time requires some tuning to invoke an underflow error,
            # depending on the platform.
            time.sleep(1)
            stream.write('\x00\x00\x00\x00', exception_on_underflow=True)

        self.assertEqual(err.exception.errno, pyaudio.paOutputUnderflowed)
        self.assertEqual(err.exception.strerror, 'Output underflowed')

    # It's difficult to invoke an underflow on ALSA, so skip.
    @unittest.skipIf('linux' in sys.platform,
                     'skipping underflow test on linux.')
    @unittest.skipIf(SKIP_HW_TESTS, 'audio hardware required.')
    def test_read_overflow_exception(self):
        stream = self.p.open(channels=1,
                             rate=44100,
                             format=pyaudio.paInt16,
                             input=True)
        time.sleep(0.5)
        stream.read(2, exception_on_overflow=False)

        with self.assertRaises(IOError) as err:
            time.sleep(0.5)
            stream.read(2, exception_on_overflow=True)

        self.assertEqual(err.exception.errno, pyaudio.paInputOverflowed)
        self.assertEqual(err.exception.strerror, 'Input overflowed')
