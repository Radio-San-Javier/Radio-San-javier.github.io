import json
import time
import urllib.request
from datetime import datetime, timezone, timedelta

URL = "https://rem.cba.gov.ar/Server/descargas/mediciones_flat.json"
ART = timezone(timedelta(hours=-3))
INTENTOS = 3
TIMEOUT = 30


def fetch():
    req = urllib.request.Request(
        f"{URL}?nocache={int(time.time())}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    for intento in range(1, INTENTOS + 1):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return json.load(r)
        except Exception as e:
            print(f"Intento {intento}/{INTENTOS} fallido: {e}")
            if intento < INTENTOS:
                time.sleep(5)
    raise SystemExit("No se pudo obtener datos tras varios intentos")


data = fetch()

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
