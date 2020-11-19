#!/usr/bin/env bash

set -e
set -x

black vyz tests --check
isort vyz tests bin --check-only
flake8 vyz tests
mypy vyz
