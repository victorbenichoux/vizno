#!/usr/bin/env bash

set -e
set -x

black vizno tests examples/api examples/reports --check
isort vizno tests examples/api examples/reports --check-only
flake8 vizno tests examples/api examples/reports
mypy vizno tests examples/api examples/reports

npm run tsc
npm run lint
