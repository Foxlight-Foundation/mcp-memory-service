#!/usr/bin/env bash
set -euo pipefail

OUT_DIR="${1:-./backups}"
TS="$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUT_DIR/$TS"

docker run --rm \
  -v two-container_qdrant_data:/data:ro \
  -v "$(pwd)/$OUT_DIR/$TS":/backup \
  alpine sh -c "cd /data && tar czf /backup/qdrant-data.tgz ."

echo "Qdrant backup complete: $OUT_DIR/$TS/qdrant-data.tgz"
