#!/bin/bash

CIBW_SKIP="cp36*" CIBW_BUILD="cp3*" cibuildwheel --platform windows