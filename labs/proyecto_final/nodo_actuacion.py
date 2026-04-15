#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import time

class NodoActuacion(Node):
    def __init__(self):
        super().__init__('nodo_actuacion')

        # 1. --- CONFIGURACIÓN DEL CONTROLADOR DIFUSO (LAB 3.4) ---
        distancia = ctrl.Antecedent(np.arange(0, 3.1, 0.01), "distancia")
        velocidad = ctrl.Consequent(np.arange(0, 1.01, 0.01), "velocidad") # Subido a 1.0 para que corra

        # Funciones de pertenencia
        distancia["muy_cerca"] = fuzz.trimf(distancia.universe, [0.0, 0.0, 0.5])
        distancia["cerca"] = fuzz.trimf(distancia.universe, [0.2, 0.6, 1.0])
        distancia["media"] = fuzz.trimf(distancia.universe, [0.7, 1.2, 1.7])
        distancia["lejos"] = fuzz.trimf(distancia.universe, [1.4, 2.0, 2.6])
        distancia["muy_lejos"] = fuzz.trimf(distancia.universe, [2.3, 3.0, 3.0])

        velocidad["parado"] = fuzz.trimf(velocidad.universe, [0.00, 0.00, 0.05])
        velocidad["lento"] = fuzz.trimf(velocidad.universe, [0.03, 0.15, 0.30])
        velocidad["medio"] = fuzz.trimf(velocidad.universe, [0.25, 0.45, 0.65])
        velocidad["rapido"] = fuzz.trimf(velocidad.universe, [0.60, 0.80, 1.00])
        velocidad["max"] = fuzz.trimf(velocidad.universe, [0.90, 1.00, 1.00])

        # Reglas
        reglas = [
            ctrl.Rule(distancia["muy_cerca"], velocidad["parado"]),
            ctrl.Rule(distancia["cerca"], velocidad["lento"]),
            ctrl.Rule(distancia["media"], velocidad["medio"]),
            ctrl.Rule(distancia["lejos"], velocidad["rapido"]),
            ctrl.Rule(distancia["muy_lejos"], velocidad["max"])
        ]
        
        self.simulador = ctrl.ControlSystemSimulation(ctrl.ControlSystem(reglas))

        # 2. --- LÓGICA DE PATRULLA A -> B ---
        self.modo_actual = "TRANSPORTE"
        self.distancia_minima = 3.0
        self.estado_patrulla = "AVANZANDO" # AVANZANDO o ROTANDO
        self.tiempo_tramo = 8.0            # Segundos que camina antes de volver
        self.tiempo_giro = 3.2             # Segundos para girar 180º aprox
        self.ultima_transicion = time.time()

        # 3. --- ROS 2 ---
        self.sub_modo = self.create_subscription(String, '/modo_operacion', self.cb_modo, 10)
        self.sub_scan = self.create_subscription(LaserScan, '/scan', self.cb_scan, 10)
        self.pub_vel = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # Timer a 20Hz para que sea reactivo
        self.create_timer(0.05, self.bucle_control)
        
        self.get_logger().info('Nodo Actuador completo iniciado. Patrulla A-B activa.')

    def cb_modo(self, msg):
        self.modo_actual = msg.data

    def cb_scan(self, msg):
        # Filtro de seguridad para el frente
        validos = [r for r in msg.ranges if msg.range_min < r < msg.range_max]
        self.distancia_minima = min(validos) if validos else 3.0

    def bucle_control(self):
        msg_vel = Twist()
        ahora = time.time()

        # --- NIVEL 1: PRIORIDADES CRÍTICAS (SISTEMA EXPERTO) ---
        if self.modo_actual == "PARADA_TERMICA":
            self.detener_robot(msg_vel, "!!! EXCESO TEMPERATURA !!!")
            return
            
        if self.modo_actual == "RECARGA":
            self.detener_robot(msg_vel, "BATERÍA BAJA: Esperando recarga...")
            return

        if self.modo_actual == "EVASION":
            msg_vel.angular.z = 0.8 # Giro rápido de emergencia
            self.pub_vel.publish(msg_vel)
            return

        # --- NIVEL 2: LÓGICA DE RUTA (TRANSPORTE) ---
        if self.estado_patrulla == "AVANZANDO":
            if ahora - self.ultima_transicion > self.tiempo_tramo:
                self.estado_patrulla = "ROTANDO"
                self.ultima_transicion = ahora
            else:
                # Calculamos velocidad lineal con LÓGICA DIFUSA
                try:
                    self.simulador.input["distancia"] = self.distancia_minima
                    self.simulador.compute()
                    msg_vel.linear.x = self.simulador.output["velocidad"]
                except:
                    msg_vel.linear.x = 0.2
                msg_vel.angular.z = 0.0

        elif self.estado_patrulla == "ROTANDO":
            if ahora - self.ultima_transicion > self.tiempo_giro:
                self.estado_patrulla = "AVANZANDO"
                self.ultima_transicion = ahora
            else:
                msg_vel.linear.x = 0.0
                msg_vel.angular.z = 1.0 # Velocidad de rotación constante

        self.pub_vel.publish(msg_vel)

    def detener_robot(self, msg, motivo):
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.pub_vel.publish(msg)
        self.get_logger().warn(motivo)

def main(args=None):
    rclpy.init(args=args)
    nodo = NodoActuacion()
    try:
        rclpy.spin(nodo)
    except KeyboardInterrupt:
        nodo.detener_robot(Twist(), "Interrupción de usuario")
    finally:
        nodo.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()