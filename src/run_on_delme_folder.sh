#!/usr/bin/env bash

set -euo pipefail


TMP_FILE="$(mktemp)"

./src/build.sh > "${TMP_FILE}"

chmod +x "${TMP_FILE}"

export CURL_SSL=""
export NOT_MISTER="true"

"${TMP_FILE}"
