import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String


class NodoPercepcion(Node):
    def __init__(self):
        super().__init__('nodo_percepcion')

        self.sub_scan = self.create_subscription(
            LaserScan,
            '/scan',
            self.callback_scan,
            10
        )

        self.pub_estado = self.create_publisher(
            String,
            '/estado_entorno',
            10
        )

        # Umbral para decidir si hay obstáculo delante
        self.umbral_obstaculo = 0.5

        self.get_logger().info('NodoPercepcion iniciado. Escuchando /scan...')

    def callback_scan(self, msg: LaserScan) -> None:
        # En TurtleBot, el frente suele corresponder a los primeros y últimos índices
        sector_frontal = list(msg.ranges[:10]) + list(msg.ranges[-10:])

        # Filtrar valores inválidos
        validos = [
            v for v in sector_frontal
            if math.isfinite(v) and msg.range_min < v < msg.range_max
        ]

        if not validos:
            estado = 'LIBRE'
            distancia_min = msg.range_max
        else:
            distancia_min = min(validos)
            estado = 'OBSTACULO' if distancia_min < self.umbral_obstaculo else 'LIBRE'

        salida = String()
        salida.data = estado
        self.pub_estado.publish(salida)

        self.get_logger().info(
            f'Estado: {estado} | Distancia frontal mínima: {distancia_min:.3f} m'
        )


def main(args=None):
    rclpy.init(args=args)
    nodo = NodoPercepcion()
    rclpy.spin(nodo)
    nodo.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()