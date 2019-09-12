#!/usr/bin/env bash

# This script is run as the default procedure for testing
# in the docker container
set -e

service mongodb start

# Run nosetests
nosetests --with-xunit --all-modules --traverse-namespace \
    --with-coverage --cover-package=mof_tda --cover-inclusive

# Generate coverage
python -m coverage xml --include=mof_tda*

# Do linting
pylint -f parseable -d I0011,R0801 mof_tda | tee pylint.out

