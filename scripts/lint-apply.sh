#!/usr/bin/env bash

set -e
set -x

black vyz tests examples
isort vyz tests examples
