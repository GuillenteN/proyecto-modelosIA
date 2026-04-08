#!/usr/bin/env python3

memoria_trabajo = {
    "temperatura_gpu": 85,
    "carga_cpu": 95,
    "robot_movimiento": True,
    "operario_cerca": False,
}

base_conocimiento = [
    {
        "nombre": "Alerta sobrecalentamiento",
        "condicion": lambda f: f["temperatura_gpu"] > 80 and f["robot_movimiento"],
        "accion": "Reducir velocidad de motores y activar ventiladores al maximo",
    },
    {
        "nombre": "Modo ahorro de energia",
        "condicion": lambda f: not f["robot_movimiento"] and f["carga_cpu"] < 10,
        "accion": "Entrar en estado de suspension",
    },
    {
        "nombre": "Parada por seguridad humana",
        "condicion": lambda f: f["operario_cerca"] and f["robot_movimiento"],
        "accion": "Reducir velocidad al 30% y activar modo colaborativo",
    },
]

print("--- Ejecutando Motor de Inferencia ---")
print(f"Hechos actuales: {memoria_trabajo}\n")

alguna_disparada = False
for regla in base_conocimiento:
    if regla["condicion"](memoria_trabajo):
        print(f"[DISPARADA] {regla['nombre']}")
        print(f"            -> Accion: {regla['accion']}\n")
        alguna_disparada = True

if not alguna_disparada:
    print("Ninguna regla activada. Sistema en estado nominal.")
