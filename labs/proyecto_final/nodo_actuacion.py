import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class NodoActuacion(Node):
    def __init__(self):
        super().__init__('nodo_actuacion')

        # 1. Configuración del Controlador Difuso (Lab 3.4)
        distancia = ctrl.Antecedent(np.arange(0, 3.1, 0.01), "distancia")
        velocidad = ctrl.Consequent(np.arange(0, 0.51, 0.01), "velocidad")

        distancia["muy_cerca"] = fuzz.trimf(distancia.universe, [0.0, 0.0, 0.5])
        distancia["cerca"] = fuzz.trimf(distancia.universe, [0.2, 0.6, 1.0])
        distancia["media"] = fuzz.trimf(distancia.universe, [0.7, 1.2, 1.7])
        distancia["lejos"] = fuzz.trimf(distancia.universe, [1.4, 2.0, 2.6])
        distancia["muy_lejos"] = fuzz.trimf(distancia.universe, [2.3, 3.0, 3.0])

        velocidad["parado"] = fuzz.trimf(velocidad.universe, [0.00, 0.00, 0.05])
        velocidad["lento"] = fuzz.trimf(velocidad.universe, [0.03, 0.10, 0.20])
        velocidad["medio"] = fuzz.trimf(velocidad.universe, [0.15, 0.25, 0.35])
        velocidad["rapido"] = fuzz.trimf(velocidad.universe, [0.30, 0.40, 0.50])
        velocidad["max"] = fuzz.trimf(velocidad.universe, [0.45, 0.50, 0.50])

        regla1 = ctrl.Rule(distancia["muy_cerca"], velocidad["parado"])
        regla2 = ctrl.Rule(distancia["cerca"], velocidad["lento"])
        regla3 = ctrl.Rule(distancia["media"], velocidad["medio"])
        regla4 = ctrl.Rule(distancia["lejos"], velocidad["rapido"])
        regla5 = ctrl.Rule(distancia["muy_lejos"], velocidad["max"])

        self.sistema = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5])
        self.simulador = ctrl.ControlSystemSimulation(self.sistema)

        # 2. Variables de estado
        self.modo_actual = "TRANSPORTE"
        self.distancia_minima = 3.0 # Por defecto lejos

        # 3. Suscriptores y Publicadores
        self.sub_modo = self.create_subscription(String, '/modo_operacion', self.cb_modo, 10)
        self.sub_scan = self.create_subscription(LaserScan, '/scan', self.cb_scan, 10)
        self.pub_vel = self.create_publisher(Twist, '/cmd_vel', 10)

        # Timer de control a 10Hz
        self.create_timer(0.1, self.bucle_control)
        
        self.get_logger().info('Nodo Actuación Difuso Operativo')

    def cb_modo(self, msg):
        self.modo_actual = msg.data

    def cb_scan(self, msg):
        # Filtramos para obtener la distancia mínima frontal
        lecturas = [r for r in msg.ranges if msg.range_min < r < msg.range_max]
        if lecturas:
            self.distancia_minima = min(lecturas)

    def bucle_control(self):
        cmd = Twist()
        
        # --- TABLA DE PRIORIDADES ACTUALIZADA ---
        
        # 1. PARADA_TERMICA: Bloqueo total por seguridad hardware
        if self.modo_actual == "PARADA_TERMICA":
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.get_logger().error("ALERTA: Parada térmica activa. Robot bloqueado.")

        # 2. RECARGA: Quieto para facilitar la conexión/carga
        elif self.modo_actual == "RECARGA":
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.get_logger().warn("MODO RECARGA: Robot estacionado.")

        # 3. EVASION: Prioridad de movimiento para no chocar
        elif self.modo_actual == "EVASION":
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5 
            self.get_logger().info("EVADIENDO: Girando para evitar obstáculo...")

        # 4. TRANSPORTE: Control Difuso (Lab 3.4)
        else:
            try:
                self.simulador.input["distancia"] = self.distancia_minima
                self.simulador.compute()
                v_difusa = self.simulador.output["velocidad"]
                
                cmd.linear.x = v_difusa
                cmd.angular.z = 0.0
                # Solo logueamos si se está moviendo de verdad
                if v_difusa > 0.05:
                    self.get_logger().info(f"TRANSPORTE: V_difusa = {v_difusa:.2f} m/s")
            except Exception as e:
                self.get_logger().error(f"Error en motor difuso: {e}")
                cmd.linear.x = 0.0

        # Publicación única al final del flujo de decisión
        self.pub_vel.publish(cmd)
        
def main(args=None):
    rclpy.init(args=args)
    nodo = NodoActuacion()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        nodo.pub_vel.publish(Twist())
    finally:
        nodo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()