import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import random
import sys

class NodoTelemetria(Node):
    def __init__(self, forzar_baja=False):
        super().__init__('nodo_telemetria')
        
        self.publisher_ = self.create_publisher(String, '/telemetria', 10)
        
        # Lógica de validación forzada
        if forzar_baja:
            self.bateria = 10.0
            self.get_logger().warn('!!! MODO PRUEBA: Batería forzada a nivel bajo (10.0) !!!')
        else:
            self.bateria = 100.0
            
        self.consumo = 0.5
        self.create_timer(1.0, self.timer_callback)
        self.get_logger().info('Nodo Telemetría listo.')

    def timer_callback(self):
        if self.bateria > 0:
            self.bateria -= self.consumo
            
        temp = random.gauss(70.0, 8.0)
        
        payload = {
            "bateria": round(self.bateria, 2),
            "temperatura": round(temp, 2),
            "status": "CRITICAL" if self.bateria < 15 else "OK"
        }
        
        msg = String()
        msg.data = json.dumps(payload)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Pub: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    
    # Comprobar si el argumento está en la llamada
    forzar = '--forzar-bateria-baja' in sys.argv
    
    nodo = NodoTelemetria(forzar_baja=forzar)
    
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        pass
    finally:
        nodo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()