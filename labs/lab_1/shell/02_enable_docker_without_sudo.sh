#!/usr/bin/env bash
set -euo pipefail

sudo usermod -aG docker "$USER"
echo "[OK] Usuario agregado al grupo docker. Cierra y abre terminal para aplicar el cambio."
