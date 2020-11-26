
#!/usr/bin/env bash

set -e
set -x

npx rollup vizno/js/vizno-core.js --format cjs | npx terser -c -m > vizno/statics/vizno-core.min.js
