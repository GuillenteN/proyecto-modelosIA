#!/usr/bin/env python3

# Laboratorio 1.1 — Análisis de Morfologías y Grados de Libertad (DoF)
#
# Tarea del PDF sección 1.1.4:
#   - Elegir un robot comercial (UR5 o TurtleBot3).
#   - Determinar tipo de articulaciones, DoF, alcance máximo y carga útil.
#   - Responder: ¿Podría este robot realizar una tarea de soldadura en el techo
#     de un coche? Justifica según sus DoF.

ROBOTS = [
    {
        "nombre": "Universal Robots UR5",
        "tipo": "Manipulador Antropomorfico",
        "articulaciones": ["R", "R", "R", "R", "R", "R"],
        "dof": 6,
        "alcance_mm": 850,
        "payload_kg": 5.0,
        "descripcion": "Cobot de 6 DoF ideal para ensamblaje y soldadura.",
    },
    {
        "nombre": "TurtleBot3 Burger",
        "tipo": "Robot Movil (AMR) - Traccion Diferencial",
        "articulaciones": ["continua_izq", "continua_der"],
        "dof": 2,
        "alcance_mm": None,
        "payload_kg": 1.0,
        "descripcion": "Robot movil de 2 ruedas, no puede posicionar herramienta en 3D.",
    },
    {
        "nombre": "Robot Cartesiano XYZ",
        "tipo": "Manipulador Cartesiano",
        "articulaciones": ["P", "P", "P"],
        "dof": 3,
        "alcance_mm": 1000,
        "payload_kg": 10.0,
        "descripcion": "3 DoF prismáticos (X, Y, Z). No puede orientar herramienta.",
    },
    {
        "nombre": "Epson SCARA T3",
        "tipo": "Manipulador SCARA",
        "articulaciones": ["R", "R", "P", "R"],
        "dof": 4,
        "alcance_mm": 400,
        "payload_kg": 3.0,
        "descripcion": "Muy rapido en el plano horizontal. Orientacion vertical fija.",
    },
]

# Articulaciones: R = Revoluta (giro), P = Prismatica (deslizamiento)
TIPO_ARTICULACION = {"R": "Revoluta (giro)", "P": "Prismatica (deslizamiento)"}


def analizar_robot(robot):
    print(f"\n{'='*55}")
    print(f"Robot: {robot['nombre']}")
    print(f"Tipo:  {robot['tipo']}")
    print(f"DoF:   {robot['dof']}")
    print(f"Articulaciones: {robot['articulaciones']}")
    for a in set(robot["articulaciones"]):
        if a in TIPO_ARTICULACION:
            print(f"  {a} = {TIPO_ARTICULACION[a]}")
    if robot["alcance_mm"]:
        print(f"Alcance max:  {robot['alcance_mm']} mm")
    print(f"Carga util:   {robot['payload_kg']} kg")
    print(f"Descripcion:  {robot['descripcion']}")


def evaluar_tarea_soldadura(robot):
    # Para posicionar y orientar una herramienta en el espacio 3D se necesitan 6 DoF.
    #   3 DoF de posicion (x, y, z)
    #   3 DoF de orientacion (roll, pitch, yaw)
    # Una tarea de soldadura en el techo de un coche requiere llegar a un punto
    # con orientacion descendente (herramienta apuntando cara arriba) => 6 DoF minimo.
    puede = robot["dof"] >= 6
    if puede:
        razon = f"Con {robot['dof']} DoF puede alcanzar cualquier punto con cualquier orientacion."
    else:
        razon = (
            f"Con solo {robot['dof']} DoF no puede controlar posicion Y orientacion "
            f"al mismo tiempo. Necesita 6 DoF para orientar la antorcha hacia arriba "
            f"en el techo del coche."
        )
    return puede, razon


print("="*55)
print("Laboratorio 1.1 — Morfologias de Robots y Analisis DoF")
print("="*55)

for robot in ROBOTS:
    analizar_robot(robot)

print(f"\n{'='*55}")
print("PREGUNTA: ¿Puede realizar una tarea de soldadura en el techo de un coche?")
print("="*55)

for robot in ROBOTS:
    puede, razon = evaluar_tarea_soldadura(robot)
    estado = "SI" if puede else "NO"
    print(f"\n[{estado}] {robot['nombre']}")
    print(f"    {razon}")

print(f"\n{'='*55}")
print("CONCLUSION:")
print("  Solo los robots con 6 DoF (o mas) pueden posicionar la herramienta")
print("  en cualquier punto del espacio con cualquier orientacion.")
print("  El UR5 (6 DoF) es apto. TurtleBot3, Cartesiano (3 DoF) y SCARA (4 DoF) no.")
print("="*55)
