#!/bin/bash

make clean
W_DIR="wheelhouse"
if [[ -d "$W_DIR" && "$(ls -A $W_DIR)" ]]
then
    mv wheelhouse "${W_DIR}_$(date +"%H-%M-%S")"
fi
mkdir "$W_DIR"

cd "portaudio_v19/"
[ -d lib_dist ] || mkdir lib_dist

#x64
make clean
dos2unix libtool
make clean
./configure --with-winapi=wasapi,wmme,directx --enable-shared=no --host=x86_64-w64-mingw32
dos2unix libtool
make onlylib
cp lib/.libs/libportaudio.a lib_dist/libportaudio-x86_64.a

#x32
make clean
dos2unix libtool
make clean
./configure --with-winapi=wasapi,wmme,directx --enable-shared=no --host=i686-w64-mingw32
dos2unix libtool
make onlylib
cp lib/.libs/libportaudio.a lib_dist/libportaudio-x86.a

export PAWP_C_C_FLAG="TRUE"
