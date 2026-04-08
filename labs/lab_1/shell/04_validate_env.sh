#!/usr/bin/env bash
set -euo pipefail

echo "[Lab1] Ejecutando validacion dentro del contenedor ros2-curso:v2 ..."
docker run -it --rm \
  -v "$PWD:/workspace_repo" \
  ros2-curso:v2 \
  bash -lc "source /opt/ros/humble/setup.bash && python3 /workspace_repo/labs/lab_1/lab_1_validacion_entorno.py"
