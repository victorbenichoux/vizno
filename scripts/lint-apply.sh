#!/usr/bin/env bash

set -e
set -x

black vyz tests bin
isort vyz tests bin
