#!/usr/bin/env bash

set -e
set -x

black vizno tests examples
isort vizno tests examples

npm run prettier:fix