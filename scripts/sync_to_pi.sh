#!/usr/bin/env bash
# Sync project source to Raspberry Pi without venv, sensor data, or Cursor metadata.
#
# Usage:
#   ./scripts/sync_to_pi.sh pi@raspberrypi.local ~/eNose_methane
#
# Requires: rsync on the machine running this script.

set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <user@host> <remote-path>" >&2
  exit 1
fi

REMOTE="$1"
DEST="$2"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

rsync -av --delete \
  --exclude '.venv/' \
  --exclude 'venv/' \
  --exclude '__pycache__/' \
  --exclude '.pytest_cache/' \
  --exclude '.cursor/' \
  --exclude 'reading/data/*.npz' \
  --exclude 'reading/data/*.csv' \
  --exclude 'acquisition/processed_data/' \
  --exclude 'program/cloud_config.json' \
  --exclude 'cloud/upload_queue.json' \
  --exclude 'credentials.json' \
  --exclude 'token.json' \
  --exclude '**/gdrive_service_account.json' \
  --exclude '**/*service_account*.json' \
  --exclude '.git/' \
  "${ROOT}/" "${REMOTE}:${DEST}/"

echo "Synced to ${REMOTE}:${DEST}"
