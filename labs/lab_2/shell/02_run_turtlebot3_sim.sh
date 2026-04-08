#!/usr/bin/env bash
set -euo pipefail

xhost +local:docker || true

if docker ps -a --format '{{.Names}}' | grep -q '^ros2_sim$'; then
	docker rm -f ros2_sim >/dev/null 2>&1 || true
fi

docker compose up -d ros2_v2

docker compose exec ros2_v2 bash
