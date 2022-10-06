#!/usr/bin/env bash

set -euo pipefail


TMP_FILE="$(mktemp)"

echo "Building..."
./src/build.sh > "${TMP_FILE}"

chmod +x "${TMP_FILE}"

export CURL_SSL=""
export LOCATION_STR="$(pwd)"
export DEBUG="true"

echo "Running..."
echo "LOCATION_STR=${LOCATION_STR}"

"${TMP_FILE}"
