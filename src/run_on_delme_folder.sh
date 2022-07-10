#!/usr/bin/env bash

set -euo pipefail


TMP_FILE="$(mktemp)"

./src/build.sh > "${TMP_FILE}"

chmod +x "${TMP_FILE}"

mkdir -p delme/Scripts
export CURL_SSL=""
export INI_PATH="delme/Scripts/update_all.ini"
export NOT_MISTER="true"

"${TMP_FILE}"
