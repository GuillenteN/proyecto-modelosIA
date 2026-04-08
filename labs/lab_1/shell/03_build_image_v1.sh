#!/usr/bin/env bash
set -euo pipefail

echo "[INFO] Este script se mantiene por compatibilidad."
echo "[INFO] A partir de ahora se recomienda construir una sola imagen final: ros2-curso:v2"

"$(dirname "$0")/../../lab_2/shell/01_build_image_v2.sh" "${1:-$HOME/ros2_curso}"
