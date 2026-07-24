# Radio San Javier

Sitio web de Radio San Javier, hecho con [Hugo](https://gohugo.io/) y el tema Blowfish.

## Datos del sitio (`/data`)

La carpeta `data/` contiene archivos JSON que alimentan partes dinámicas del sitio. La idea es cambiar estos archivos cuando se quiere modificar información estructurada sin tocar templates HTML.

### `data/radio.json`

Datos generales de la radio y del streaming en vivo.

Se usa en:

- el reproductor embebido de la home;
- el reproductor popup `/radio-player.html`.

Campos principales:

```json
{
  "name": "Radio San Javier",
  "frequency": "89.3 FM",
  "tagline": "La radio del pueblo",
  "streamUrl": "https://.../stream",
  "streamType": "audio/mpeg"
}
```

Para cambiar la URL del streaming, modificar `streamUrl`.

---

### `data/grilla.json`

Define la programación semanal de la radio.

Se usa en:

- la grilla completa de programación;
- la tira de programación del día en la home.

Campos importantes:

- `titulo`: título de la grilla.
- `leyenda`: tipos de programa y textos explicativos.
- `horas`: horas visibles en la tabla.
- `dias`: nombres de los días.
- `programas`: lista de programas.

Cada programa tiene esta forma:

```json
{
  "nombre": "Es lo que hay",
  "hora_inicio": 10,
  "duracion": 2,
  "dias": [0, 1, 2, 3, 4],
  "tipo": "radio_sanjavier",
  "link": "/programas/es_lo_que_hay/"
}
```

#### Índice de días

En `dias`, los números significan:

| Número | Día |
|---:|---|
| 0 | Lunes |
| 1 | Martes |
| 2 | Miércoles |
| 3 | Jueves |
| 4 | Viernes |
| 5 | Sábado |
| 6 | Domingo |

#### Tipos de programa

Los tipos usados actualmente son:

- `radio_sanjavier`: programas hechos en Radio San Javier.
- `retransmitido`: programas retransmitidos.
- `musical`: franjas musicales.

El campo `link` es opcional. Si se agrega, el programa queda clickeable en la grilla.

---

### `data/publicidades.json`

Define anunciantes/publicidades.

Se usa en el partial de publicidades para mostrar anuncios según ubicación.

Ejemplo:

```json
{
  "nombre": "Almacén Don Pepe",
  "imagen": "/publicidades/almacen-don-pepe.svg",
  "link": "#",
  "activo": true,
  "ubicaciones": ["home", "es_lo_que_hay"]
}
```

Campos:

- `nombre`: nombre del anunciante.
- `imagen`: ruta pública de la imagen. Normalmente apunta a archivos dentro de `static/publicidades/`.
- `link`: URL de destino al hacer click.
- `activo`: `true` para mostrar, `false` para ocultar sin borrar.
- `ubicaciones`: lugares donde se muestra la publicidad.

Ubicaciones usadas actualmente:

- `home`: publicidades en la home.
- `es_lo_que_hay`: publicidades asociadas al programa Es lo que hay.

---

### `data/clima.json`

Contiene datos de clima mostrados en la home.

Este archivo se actualiza automáticamente con GitHub Actions usando Open-Meteo.

Archivos relacionados:

- `.github/workflows/clima.yml`
- `scripts/actualizar_clima.py`

No conviene editarlo a mano salvo para pruebas puntuales.

Campos actuales:

```json
{
  "Temperatura": 12.9,
  "Humedad": 61.0,
  "Velocidad de Viento": 1.75,
  "Registro de lluvia": 0.0,
  "actualizado": "24/7 12:25"
}
```

## Reglas generales

- No editar `public/` a mano: es salida generada por Hugo.
- No editar `themes/blowfish/` salvo que sea estrictamente necesario.
- Para cambiar contenido editorial, usar `content/`.
- Para cambiar datos estructurados como programación, publicidades, clima o streaming, usar `data/`.

## Desarrollo local

Si tenés Hugo instalado:

```bash
hugo server -D
```

Luego abrir la URL local que indique Hugo.
