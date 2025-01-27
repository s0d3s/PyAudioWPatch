#!/bin/bash

FORCE_CYGWIN_ENV=true PYTHONUTF8=1 CIBW_SKIP="cp36*" CIBW_BUILD="cp3*" cibuildwheel --platform windows
