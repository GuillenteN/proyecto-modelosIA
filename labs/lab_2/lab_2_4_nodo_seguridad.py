#!/usr/bin/env python3

import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class SeguridadRobot(Node):
    def __init__(self):
        super().__init__("nodo_seguridad")
        self.publisher_ = self.create_publisher(Twist, "cmd_vel", 10)
        self.subscription = self.create_subscription(
            LaserScan, "scan", self.listener_callback, 10
        )
        self.stop_dist = 0.40
        self.slow_dist = 0.85
        self.clear_dist = 1.20
        self.max_linear = 0.12
        self.min_linear = 0.04
        self.max_angular = 1.2
        self.side_safe_dist = 0.26
        self.front_side_safe_dist = 0.30
        self.turning_side = 1.0
        self.recovery_until_ns = 0
        self.recovery_phase = "none"
        self.reverse_duration_ns = int(0.45 * 1e9)
        self.turn_duration_ns = int(0.85 * 1e9)
        self.get_logger().info("Nodo SeguridadRobot iniciado.")

    @staticmethod
    def _valid_ranges(values, rmin, rmax):
        out = []
        for v in values:
            if math.isfinite(v) and rmin < v < rmax:
                out.append(v)
        return out

    @staticmethod
    def _safe_min(values, default):
        return min(values) if values else default

    @staticmethod
    def _safe_avg(values, default):
        return sum(values) / len(values) if values else default

    def listener_callback(self, msg):
        now_ns = self.get_clock().now().nanoseconds
        n = len(msg.ranges)
        if n < 10:
            return

        # En TurtleBot3 el frente suele estar en el inicio/final del barrido.
        # Usamos sectores amplios para evitar decisiones inestables por ruido.
        front_span = max(10, int(0.08 * n))
        side_span = max(20, int(0.18 * n))
        fside_span = max(14, int(0.12 * n))

        raw_front = list(msg.ranges[:front_span]) + list(msg.ranges[-front_span:])
        raw_front_left = list(msg.ranges[front_span : front_span + fside_span])
        raw_front_right = list(msg.ranges[n - front_span - fside_span : n - front_span])
        raw_left = list(msg.ranges[int(0.25 * n) : int(0.25 * n) + side_span])
        raw_right = list(msg.ranges[int(0.75 * n) : int(0.75 * n) + side_span])

        front_vals = self._valid_ranges(raw_front, msg.range_min, msg.range_max)
        front_left_vals = self._valid_ranges(raw_front_left, msg.range_min, msg.range_max)
        front_right_vals = self._valid_ranges(raw_front_right, msg.range_min, msg.range_max)
        left_vals = self._valid_ranges(raw_left, msg.range_min, msg.range_max)
        right_vals = self._valid_ranges(raw_right, msg.range_min, msg.range_max)

        d_front = self._safe_min(front_vals, msg.range_max)
        d_front_left = self._safe_min(front_left_vals, msg.range_max)
        d_front_right = self._safe_min(front_right_vals, msg.range_max)
        d_left = self._safe_avg(left_vals, msg.range_max)
        d_right = self._safe_avg(right_vals, msg.range_max)

        cmd = Twist()

        # Gestion de transiciones de recuperacion.
        if self.recovery_phase == "reverse" and now_ns >= self.recovery_until_ns:
            self.recovery_phase = "turn"
            self.recovery_until_ns = now_ns + self.turn_duration_ns
        elif self.recovery_phase == "turn" and now_ns >= self.recovery_until_ns:
            self.recovery_phase = "none"
            self.recovery_until_ns = 0

        # Si esta en recuperacion, mantiene la maniobra hasta terminar la ventana temporal.
        if self.recovery_phase != "none" and now_ns < self.recovery_until_ns:
            if self.recovery_phase == "reverse":
                cmd.linear.x = -0.06
                cmd.angular.z = 0.0
            else:
                cmd.linear.x = 0.0
                cmd.angular.z = self.turning_side * self.max_angular
            self.publisher_.publish(cmd)
            return

        # Activar recuperacion si hay riesgo alto de impacto frontal o en esquinas frontales.
        if (
            d_front < self.stop_dist
            or d_front_left < self.front_side_safe_dist
            or d_front_right < self.front_side_safe_dist
        ):
            self.turning_side = 1.0 if d_left >= d_right else -1.0
            self.recovery_phase = "reverse"
            self.recovery_until_ns = now_ns + self.reverse_duration_ns
            cmd.linear.x = -0.06
            cmd.angular.z = 0.0
            self.get_logger().warn(
                (
                    "Obstaculo critico "
                    f"(frente={d_front:.2f}m, fl={d_front_left:.2f}m, fr={d_front_right:.2f}m). "
                    "Activando marcha atras de seguridad."
                )
            )
        elif d_front < self.slow_dist:
            # Zona de precaucion: avanza lento y corrige direccion.
            ratio = max(0.0, min(1.0, (d_front - self.stop_dist) / (self.slow_dist - self.stop_dist)))
            cmd.linear.x = self.min_linear + ratio * (self.max_linear - self.min_linear)

            # Error lateral positivo => hay mas espacio a la izquierda.
            error_lr = d_left - d_right
            cmd.angular.z = max(-self.max_angular, min(self.max_angular, 2.0 * error_lr))
        else:
            # Campo despejado: avanza estable con correccion suave.
            cmd.linear.x = self.max_linear
            error_lr = d_left - d_right
            cmd.angular.z = max(-0.35, min(0.35, 0.6 * error_lr))

            # Si esta totalmente despejado, recentra y evita oscilaciones.
            if d_front > self.clear_dist:
                cmd.angular.z *= 0.5

        # Proteccion lateral: evita roce continuo con paredes/bordes.
        if d_left < self.side_safe_dist and d_right >= self.side_safe_dist:
            cmd.linear.x = min(cmd.linear.x, 0.04)
            cmd.angular.z = min(cmd.angular.z, -0.70)  # separarse hacia la derecha
        elif d_right < self.side_safe_dist and d_left >= self.side_safe_dist:
            cmd.linear.x = min(cmd.linear.x, 0.04)
            cmd.angular.z = max(cmd.angular.z, 0.70)  # separarse hacia la izquierda
        elif min(d_left, d_right) < self.side_safe_dist:
            # Si hay riesgo en ambos lados, priorizar control y reducir velocidad.
            cmd.linear.x = min(cmd.linear.x, 0.03)
            cmd.angular.z *= 0.6

        self.publisher_.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    nodo = SeguridadRobot()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
