#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

# Here you can place any logic that you want to execute on `entrypoint`.
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Service is up: $cmd"

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
