#!/bin/bash

set -e
set -eo pipefail

mkdir -p tests/output/Preproc
mkdir -p tests/output/climAverager
mkdir -p tests/output/climFileIO
mkdir -p tests/output/PyAverager/ice/slice
mkdir -p tests/output/PyAverager/ice/series
mkdir -p tests/output/PyAverager/atm/series
mkdir -p tests/output/PyAverager/atm/slice
mkdir -p tests/output/PyAverager/lnd/series
mkdir -p tests/output/PyAverager/lnd/slice

coverage run -p -m pytest tests/
coverage combine
coverage xml
coverage report
coverage html

rm tests/output/Preproc/* tests/output/climAverager/* tests/output/climFileIO/* tests/output/PyAverager/ice/slice/* tests/output/PyAverager/ice/series/* tests/output/PyAverager/atm/series/* tests/output/PyAverager/atm/slice/* tests/output/PyAverager/lnd/series/* tests/output/PyAverager/lnd/slice/*
