#!/usr/bin/env bash

set -e
set -x

black vyz tests bin examples --check
isort vyz tests bin examples --check-only
flake8 vyz tests bin examples
mypy vyz tests bin examples
