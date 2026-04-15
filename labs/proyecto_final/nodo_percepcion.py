import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class NodoPercepcion(Node):
    def __init__(self):
        super().__init__('nodo_percepcion')

        # Configuración de QoS para sensores (Crucial para Gazebo/Robots reales)
        qos_perfil = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        self.sub_scan = self.create_subscription(
            LaserScan,
            '/scan',
            self.callback_scan,
            qos_perfil
        )

        self.pub_estado = self.create_publisher(
            String,
            '/estado_entorno',
            10
        )

        # Umbral para decidir si hay obstáculo delante (metros)
        self.umbral_obstaculo = 0.5

        self.get_logger().info('--- NodoPercepcion Activo ---')
        self.get_logger().info(f'Umbral de detección: {self.umbral_obstaculo}m')

    def callback_scan(self, msg: LaserScan) -> None:
        # En la mayoría de Lidars (LDS-01, RPLidar), el frente es el índice 0
        # Tomamos un rango de 20 grados a cada lado
        indices_frontales = list(range(-20, 21)) 
        
        lecturas_frontales = []
        for i in indices_frontales:
            # Usamos el módulo para manejar el "wrap around" de la lista de rangos
            distancia = msg.ranges[i]
            
            # Filtramos valores no válidos (inf, nan o fuera de rango del sensor)
            if math.isfinite(distancia) and msg.range_min <= distancia <= msg.range_max:
                lecturas_frontales.append(distancia)

        # Lógica de decisión
        if not lecturas_frontales:
            # Si no hay lecturas válidas, puede que no haya nada cerca o el sensor esté fallando
            distancia_min = float('inf')
            estado = 'LIBRE (Sin datos)'
        else:
            distancia_min = min(lecturas_frontales)
            estado = 'OBSTACULO' if distancia_min < self.umbral_obstaculo else 'LIBRE'

        # Publicar el estado
        msg_salida = String()
        msg_salida.data = estado
        self.pub_estado.publish(msg_salida)

        # Log con información útil
        self.get_logger().info(
            f'[{estado}] Min: {distancia_min:.2f}m | Lecturas válidas: {len(lecturas_frontales)}'
        )

def main(args=None):
    rclpy.init(args=args)
    nodo = NodoPercepcion()
    
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        nodo.get_logger().info('Nodo detenido por el usuario.')
    finally:
        nodo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()