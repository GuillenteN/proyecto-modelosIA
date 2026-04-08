#!/usr/bin/env python3

# Laboratorio 3.1 — Identificación de Reglas de Experto
#
# Ejercicio del PDF sección 3.1.3:
# Protocolo dado:
#   "Si el LED parpadea en rojo, comprueba el voltaje.
#    Si el voltaje es inferior a 12 V, la fuente falla.
#    Si el voltaje es correcto pero el parpadeo sigue,
#    la temperatura podría ser excesiva (>90°C)."
#
# Tarea: redactar el protocolo como Hechos y Reglas formales (IF-THEN).

# --- Base de Conocimiento: Reglas IF-THEN formalizadas ---
base_conocimiento = [
    {
        "nombre": "Regla 1 — Fallo de fuente de alimentacion",
        "condicion": lambda f: f["led"] == "rojo" and f["voltaje"] < 12,
        "accion": "diagnostico = 'Fallo Fuente de Alimentacion'",
        "diagnostico": "Fallo Fuente de Alimentacion",
    },
    {
        "nombre": "Regla 2 — Temperatura excesiva",
        "condicion": lambda f: f["led"] == "rojo" and f["voltaje"] >= 12 and f["temperatura"] > 90,
        "accion": "diagnostico = 'Temperatura Excesiva'",
        "diagnostico": "Temperatura Excesiva",
    },
    {
        "nombre": "Regla 3 — Sistema nominal",
        "condicion": lambda f: f["led"] != "rojo",
        "accion": "diagnostico = 'Sistema OK'",
        "diagnostico": "Sistema OK",
    },
]

# --- Casos de prueba ---
casos = [
    {"led": "rojo",  "voltaje": 10.5, "temperatura": 75,  "caso": "LED rojo, bajo voltaje"},
    {"led": "rojo",  "voltaje": 13.2, "temperatura": 95,  "caso": "LED rojo, voltaje OK, alta temp"},
    {"led": "rojo",  "voltaje": 13.2, "temperatura": 80,  "caso": "LED rojo, voltaje OK, temp normal"},
    {"led": "verde", "voltaje": 12.8, "temperatura": 55,  "caso": "LED verde (sistema nominal)"},
]

print("="*55)
print("Laboratorio 3.1 — Extraccion de Conocimiento IF-THEN")
print("="*55)

print("\nProtocolo de experto (lenguaje natural):")
print("  Si el LED parpadea en rojo, comprueba el voltaje.")
print("  Si voltaje < 12 V  => la fuente falla.")
print("  Si voltaje OK pero LED sigue rojo y temp > 90 C => temperatura excesiva.")

print("\nReglas formalizadas (IF-THEN):")
print("  Hecho observable: led, voltaje, temperatura")
print("  Regla 1: IF (led == 'rojo') AND (voltaje < 12)            THEN 'Fallo Fuente'")
print("  Regla 2: IF (led == 'rojo') AND (voltaje >= 12)           THEN")
print("                              AND (temperatura > 90)              'Temperatura Excesiva'")
print("  Regla 3: IF (led != 'rojo')                               THEN 'Sistema OK'")

print("\n" + "="*55)
print("Ejecucion del motor de inferencia sobre casos de prueba:")
print("="*55)

for hechos in casos:
    print(f"\nCaso: {hechos['caso']}")
    print(f"  Hechos: led={hechos['led']!r}  voltaje={hechos['voltaje']} V  temp={hechos['temperatura']} C")
    resultado = None
    for regla in base_conocimiento:
        if regla["condicion"](hechos):
            resultado = regla["diagnostico"]
            print(f"  [DISPARADA] {regla['nombre']}")
            print(f"              -> {regla['accion']}")
            break
    if resultado is None:
        print("  [NINGUNA REGLA] Caso no contemplado en la base de conocimiento.")
    else:
        print(f"  => DIAGNOSTICO FINAL: {resultado}")
