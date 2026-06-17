import json
import sys
from datetime import datetime, timezone, timedelta

ART = timezone(timedelta(hours=-3))


def cargar(path):
    print(f"[parse] leyendo {path}...")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    print(f"[parse] {len(data)} estaciones")
    return data


ruta = sys.argv[1] if len(sys.argv) > 1 else "data/clima.json"
print(f"[inicio] {datetime.now(ART).strftime('%d/%m/%Y %H:%M')} ART")

data = cargar(ruta)

print("[parse] buscando estación 30551...")
est = next((e for e in data if e["id"] == "30551"), None)
if not est:
    raise SystemExit("[parse] estación 30551 no encontrada")
print(f"[parse] encontrada: {est.get('nombre', 'sin nombre')}")

ahora = datetime.now(ART)
out = {
    "Temperatura": est["Temperatura"],
    "Humedad": est["Humedad"],
    "Velocidad de Viento": est["Velocidad de Viento"],
    "Registro de lluvia": est["Registro de lluvia"],
    "actualizado": ahora.strftime("%-d/%-m %H:%M"),
}

print(f"[datos] temp={round(out['Temperatura'], 1)}°C  hum={round(out['Humedad'], 1)}%  viento={round(out['Velocidad de Viento'], 2)} m/s  lluvia={out['Registro de lluvia']} mm")

with open("data/clima.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"[ok] data/clima.json actualizado — {out['actualizado']} hs ART")
