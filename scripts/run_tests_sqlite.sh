#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../backend"
FAMPLUS_SQLITE=1 python manage.py test "$@"
