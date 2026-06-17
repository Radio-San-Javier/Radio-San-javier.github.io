import json
import time
import requests
from datetime import datetime, timezone, timedelta

URL = "https://rem.cba.gov.ar/Server/descargas/mediciones_flat.json"
ART = timezone(timedelta(hours=-3))
INTENTOS = 3
TIMEOUT = 30


def fetch():
    url = f"{URL}?nocache={int(time.time())}"
    print(f"[fetch] GET {url}")
    for intento in range(1, INTENTOS + 1):
        print(f"[fetch] intento {intento}/{INTENTOS}...")
        try:
            r = requests.get(url, timeout=TIMEOUT, headers={"User-Agent": "Mozilla/5.0"})
            print(f"[fetch] HTTP {r.status_code} — {len(r.content)} bytes")
            r.raise_for_status()
            data = r.json()
            print(f"[fetch] JSON parseado, {len(data)} estaciones")
            return data
        except Exception as e:
            print(f"[fetch] intento {intento} fallido: {e}")
            if intento < INTENTOS:
                print("[fetch] esperando 5s antes de reintentar...")
                time.sleep(5)

    raise SystemExit("[fetch] no se pudo obtener datos tras varios intentos")


print(f"[inicio] {datetime.now(ART).strftime('%d/%m/%Y %H:%M')} ART")

data = fetch()

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
