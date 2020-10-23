#!/bin/bash

set -e
set -eo pipefail


coverage run -p -m pytest tests/
coverage combine
coverage xml
coverage report
coverage html

rm tests/output/Preproc/* tests/output/climAverager/* tests/output/climFileIO/* tests/output/PyAverager/ice/slice/* tests/output/PyAverager/ice/series/* tests/output/PyAverager/atm/series/* tests/output/PyAverager/atm/slice/* tests/output/PyAverager/lnd/series/* tests/output/PyAverager/lnd/slice/*


