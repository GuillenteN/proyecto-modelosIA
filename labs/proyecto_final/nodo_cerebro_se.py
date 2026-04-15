import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json

class NodoCerebroSE(Node):
    def __init__(self):
        super().__init__('nodo_cerebro_se')

        # Estado interno del "Sistema Experto"
        self.bateria = 100.0
        self.temperatura = 70.0
        self.estado_percepcion = 'LIBRE'
        self.modo_actual = 'TRANSPORTE'

        # Suscriptores
        self.sub_telemetria = self.create_subscription(String, '/telemetria', self.cb_telemetria, 10)
        self.sub_percepcion = self.create_subscription(String, '/estado_entorno', self.cb_percepcion, 10)

        # Publicador del modo resultante
        self.pub_modo = self.create_publisher(String, '/modo_operacion', 10)

        # Timer para el motor de reglas (ejecuta a 2Hz para decidir rápido)
        self.create_timer(0.5, self.motor_inferencia)
        
        self.get_logger().info('Cerebro Sistema Experto operativo.')

    def cb_telemetria(self, msg):
        try:
            datos = json.loads(msg.data)
            self.bateria = datos.get('bateria', 100.0)
            self.temperatura = datos.get('temperatura', 70.0)
        except Exception as e:
            self.get_logger().error(f'Error parseando telemetría: {e}')

    def cb_percepcion(self, msg):
        self.estado_percepcion = msg.data

    def motor_inferencia(self):
        """Implementación del Sistema Experto (Sección 4.1)"""
        nuevo_modo = 'TRANSPORTE' # Modo por defecto

        # REGLA 1: Prioridad máxima - Seguridad Térmica
        if self.temperatura > 85:
            nuevo_modo = 'PARADA_TERMICA'
        
        # REGLA 2: Supervivencia - Recarga
        elif self.bateria < 15:
            nuevo_modo = 'RECARGA'
        
        # REGLA 3: Navegación - Evasión
        # Si hay obstáculo y el objetivo era movernos (Transporte)
        elif self.estado_percepcion == 'OBSTACULO' and nuevo_modo == 'TRANSPORTE':
            nuevo_modo = 'EVASION'

        # Publicar si hay cambio o para mantener el estado
        self.modo_actual = nuevo_modo
        msg_modo = String()
        msg_modo.data = self.modo_actual
        self.pub_modo.publish(msg_modo)
        
        self.get_logger().info(f'Estado: T:{self.temperatura:.1f} B:{self.bateria:.1f} Obs:{self.estado_percepcion} -> MODO: {self.modo_actual}')

def main(args=None):
    rclpy.init(args=args)
    nodo = NodoCerebroSE()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()