#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT_DIR"

docker build -f labs/lab_1/docker/Dockerfile.v1 -t ros2-curso:v1 .
docker build -f labs/lab_2/docker/Dockerfile.v2 -t ros2-curso:v2 .

docker images | grep -E '^ros2-curso\s+v2' || true

echo "[OK] Imagen ros2-curso:v2 creada."
