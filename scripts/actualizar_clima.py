import json
import sys
from datetime import datetime, timezone, timedelta

ART = timezone(timedelta(hours=-3))


def cargar(path):
    print(f"[parse] leyendo {path}...")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data


def numero(current, campo):
    valor = current.get(campo)
    if valor is None:
        raise SystemExit(f"[parse] falta el campo current.{campo}")
    return float(valor)


ruta = sys.argv[1] if len(sys.argv) > 1 else "/tmp/clima-openmeteo.json"
print(f"[inicio] {datetime.now(ART).strftime('%d/%m/%Y %H:%M')} ART")

# Fuente: Open-Meteo, sin API key.
# Coordenadas aproximadas de San Javier, Córdoba, Argentina.
data = cargar(ruta)
current = data.get("current")
if not isinstance(current, dict):
    raise SystemExit("[parse] respuesta inválida: falta current")

ahora = datetime.now(ART)
out = {
    "Temperatura": numero(current, "temperature_2m"),
    "Humedad": numero(current, "relative_humidity_2m"),
    "Velocidad de Viento": numero(current, "wind_speed_10m"),
    "Registro de lluvia": numero(current, "precipitation"),
    "actualizado": ahora.strftime("%-d/%-m %H:%M"),
}

print(
    f"[datos] temp={round(out['Temperatura'], 1)}°C  "
    f"hum={round(out['Humedad'], 1)}%  "
    f"viento={round(out['Velocidad de Viento'], 2)} m/s  "
    f"lluvia={out['Registro de lluvia']} mm"
)

with open("data/clima.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"[ok] data/clima.json actualizado — {out['actualizado']} hs ART")
