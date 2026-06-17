import json
import sys
import time
import urllib.request
from datetime import datetime, timezone, timedelta

URL = f"https://rem.cba.gov.ar/Server/descargas/mediciones_flat.json?nocache={int(time.time())}"
ART = timezone(timedelta(hours=-3))

try:
    with urllib.request.urlopen(URL, timeout=15) as r:
        data = json.load(r)
except Exception as e:
    raise SystemExit(f"Error al obtener datos: {e}")

est = next((e for e in data if e["id"] == "30551"), None)
if not est:
    raise SystemExit("Estación 30551 no encontrada")

ahora = datetime.now(ART)
out = {
    "Temperatura": est["Temperatura"],
    "Humedad": est["Humedad"],
    "Velocidad de Viento": est["Velocidad de Viento"],
    "Registro de lluvia": est["Registro de lluvia"],
    "actualizado": ahora.strftime("%-d/%-m %H:%M"),
}

with open("data/clima.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)

print(f"Temperatura: {round(est['Temperatura'], 1)} °C")
print(f"Actualizado: {out['actualizado']} hs (ART)")
