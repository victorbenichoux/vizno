#!/usr/bin/env bash

set -e
set -x

black vizno tests examples --check
isort vizno tests examples --check-only
flake8 vizno tests examples
mypy vizno tests examples
