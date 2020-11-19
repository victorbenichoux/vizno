#!/usr/bin/env bash

set -e
set -x

black vyz tests examples --check
isort vyz tests examples --check-only
flake8 vyz tests examples
mypy vyz tests examples
