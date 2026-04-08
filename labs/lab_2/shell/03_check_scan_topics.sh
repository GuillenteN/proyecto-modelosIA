#!/usr/bin/env bash
set -euo pipefail

if ! docker ps --format '{{.Names}}' | grep -q '^ros2_sim$'; then
	echo "[ERROR] No hay un contenedor 'ros2_sim' en ejecucion."
	echo "        Arranca primero: ./labs/lab_2/shell/02_run_turtlebot3_sim.sh"
	exit 1
fi

docker compose exec ros2_v2 bash -lc '
source /opt/ros/humble/setup.bash
echo "--- ros2 topic list (filtrado) ---"
ros2 topic list | grep -E "^/(scan|cmd_vel|tf|tf_static)$" || true

echo "--- prueba de /scan (1 mensaje, timeout 8s) ---"
if timeout 8 ros2 topic echo /scan --once; then
	echo "[OK] /scan esta publicando correctamente."
else
	echo "[WARN] /scan no disponible aun."

	if ros2 service list | grep -q "^/spawn_entity$"; then
		echo "[INFO] Intentando spawnear TurtleBot3 en Gazebo ..."
		ros2 run gazebo_ros spawn_entity.py \
			-entity burger \
			-file /opt/ros/humble/share/turtlebot3_gazebo/models/turtlebot3_burger/model.sdf \
			-x -2.0 -y -0.5 -z 0.01 || true

		echo "[INFO] Reintentando lectura de /scan ..."
		timeout 8 ros2 topic echo /scan --once || true
	else
		echo "[INFO] Servicio /spawn_entity no disponible todavia."
		echo "       Espera unos segundos y vuelve a ejecutar este script."
	fi
fi
'
