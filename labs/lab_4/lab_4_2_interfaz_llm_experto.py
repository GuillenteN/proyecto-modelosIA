#!/usr/bin/env python3

import json


def interprete_con_api_anthropic(comando_voz, api_key):
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = """Eres el modulo de interpretacion de comandos de un robot
industrial. Devuelve UNICAMENTE JSON valido con esta estructura:
{
  \"emergencia\": true/false,
  \"causa\": \"descripcion o null\",
  \"tarea\": \"navegacion\" | \"recarga\" | \"inspeccion\" | \"espera\" | null,
  \"destino\": \"nombre del lugar o null\",
  \"prioridad\": \"alta\" | \"media\" | \"baja\"
}
Si no entiendes el comando, devuelve null/false."""

    mensaje = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        system=system_prompt,
        messages=[{"role": "user", "content": comando_voz}],
    )

    respuesta_texto = mensaje.content[0].text.strip()
    try:
        return json.loads(respuesta_texto)
    except json.JSONDecodeError:
        print(f"[LLM] Error al parsear JSON: {respuesta_texto}")
        return {}


def interprete_con_ollama_local(comando_voz, modelo="llama3"):
    try:
        import ollama

        system_prompt = """Eres el modulo de interpretacion de un robot.
Devuelve SOLO JSON con: emergencia (bool), causa (str|null),
tarea (str|null), destino (str|null), prioridad (str)."""

        respuesta = ollama.chat(
            model=modelo,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": comando_voz},
            ],
        )
        texto = respuesta["message"]["content"].strip()
        return json.loads(texto)
    except ImportError:
        print("[Ollama] Libreria no instalada. Usando modo simulado.")
        return {}
    except Exception as e:
        print(f"[Ollama] Error: {e}")
        return {}


def motor_experto_seguridad(hechos):
    if not hechos:
        print("[SE] Sin Hechos que procesar o JSON invalido.")
        return

    if hechos.get("emergencia"):
        causa = hechos.get("causa", "desconocida")
        print(f"[SE] PRIORIDAD MAXIMA. Causa: {causa}")
        print("[SE] Ejecutando protocolo de evacuacion y parada de emergencia.")
    elif hechos.get("tarea") == "navegacion":
        destino = hechos.get("destino", "destino no especificado")
        prioridad = hechos.get("prioridad", "media")
        print(f"[SE] Tarea de navegacion | Destino: '{destino}' | Prioridad: {prioridad}")
        print("[SE] Comprobando bateria y ruta... Iniciando navegacion.")
    elif hechos.get("tarea") == "recarga":
        print("[SE] Tarea de recarga. Navegando a estacion de carga.")
    elif hechos.get("tarea") == "inspeccion":
        destino = hechos.get("destino", "zona no especificada")
        print(f"[SE] Tarea de inspeccion en: '{destino}'. Activando sensores.")
    else:
        print(f"[SE] Tarea recibida: {hechos}. Sin accion especifica definida.")


def interprete_simulado(comando_voz):
    print(f"[LLM-sim] Procesando: '{comando_voz}'")
    cmd = comando_voz.lower()
    if any(w in cmd for w in ["fuego", "humo", "emergencia", "caliente"]):
        return {
            "emergencia": True,
            "causa": "posible_incendio",
            "tarea": None,
            "destino": None,
            "prioridad": "alta",
        }
    if any(w in cmd for w in ["ve a", "navega a", "muevete a"]):
        destino = cmd
        for prefijo in ["muevete a ", "navega a ", "ve a "]:
            if prefijo in destino:
                destino = destino.split(prefijo, 1)[1].strip()
                break
        destino = destino.rstrip(".,!?")
        return {
            "emergencia": False,
            "causa": None,
            "tarea": "navegacion",
            "destino": destino,
            "prioridad": "media",
        }
    if any(w in cmd for w in ["recarga", "bateria", "carga"]):
        return {
            "emergencia": False,
            "causa": None,
            "tarea": "recarga",
            "destino": "base_carga",
            "prioridad": "alta",
        }
    if "inspeccion" in cmd or "revisa" in cmd:
        return {
            "emergencia": False,
            "causa": None,
            "tarea": "inspeccion",
            "destino": "zona_B",
            "prioridad": "baja",
        }
    return {}


def main():
    comandos_prueba = [
        "Cuidado, hay humo en el laboratorio!",
        "ve a la zona B del almacen",
        "necesito que te recargues ya",
        "realiza una inspeccion de la zona de montaje",
    ]

    for cmd in comandos_prueba:
        print("-" * 55)
        hechos = interprete_simulado(cmd)
        print(f"[LLM->SE] Hechos extraidos: {json.dumps(hechos, ensure_ascii=False)}")
        motor_experto_seguridad(hechos)
        print()


if __name__ == "__main__":
    main()
