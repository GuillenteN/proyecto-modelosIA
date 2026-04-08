#!/usr/bin/env bash
# Lab 2.2 — Inspección del Grafo ROS 2 y Mensajería
#
# Uso: ejecutar desde la raíz del repositorio.
# Requiere: docker compose up -d ros2_v1 (o que ya esté en marcha).
#
# Lanza automáticamente el nodo publicador demo_nodes_py talker y
# muestra los comandos de inspección que debe ejecutar el alumno en
# un segundo terminal.

set -e

SERVICE=ros2_v1

if ! docker compose ps --services --filter "status=running" 2>/dev/null | grep -q "^${SERVICE}$"; then
    echo "Arrancando servicio ${SERVICE}..."
    docker compose up -d "${SERVICE}"
    sleep 2
fi

echo ""
echo "=== Lab 2.2 — Inspección del Grafo ROS 2 ==="
echo ""
echo "Terminal 1 (este terminal): lanzando nodo publicador..."
echo "  Ejecuta: ros2 run demo_nodes_py talker"
echo ""
echo "Abre un SEGUNDO terminal y ejecuta los comandos de inspección:"
echo ""
echo "  docker compose exec ${SERVICE} bash"
echo ""
echo "  # Dentro del contenedor (Terminal 2):"
echo "  ros2 node list                          # Lista nodos activos"
echo "  ros2 topic list                         # Lista tópicos activos"
echo "  ros2 topic echo /chatter                # Ver mensajes en tiempo real"
echo "  ros2 topic hz /chatter                  # Ver frecuencia de publicación"
echo "  ros2 interface show std_msgs/msg/String # Estructura del mensaje"
echo ""
echo "Resultados esperados:"
echo "  ros2 node list   => /talker"
echo "  ros2 topic list  => /chatter"
echo "  ros2 topic hz    => average rate: 1.000"
echo ""

docker compose exec "${SERVICE}" bash -lc "ros2 run demo_nodes_py talker"
