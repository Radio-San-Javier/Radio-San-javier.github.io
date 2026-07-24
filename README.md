# Radio San Javier

Sitio web de Radio San Javier, hecho con [Hugo](https://gohugo.io/) y el tema Blowfish.

## Desarrollo local

```bash
hugo server -D
```

Luego abrir la URL local que indique Hugo.

## Reglas generales

- No editar `public/` a mano: es salida generada por Hugo.
- No editar `themes/blowfish/` salvo que sea estrictamente necesario.
- Para cambiar contenido editorial, usar `content/`.
- Para cambiar datos estructurados como programación, publicidades, clima o streaming, usar `data/`.
- Para episodios/podcasts, usar páginas dentro de `content/programas/<programa>/<episodio>/index.md`.

---

## Datos del sitio (`/data`)

La carpeta `data/` contiene archivos JSON que alimentan partes dinámicas del sitio. La idea es cambiar estos archivos cuando se quiere modificar información estructurada sin tocar templates HTML.

### `data/radio.json`

Datos generales de la radio y del streaming en vivo.

Se usa en:

- el reproductor embebido de la home;
- el reproductor popup `/radio-player.html`.

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

- `radio_sanjavier`: programas hechos en Radio San Javier.
- `retransmitido`: programas retransmitidos.
- `musical`: franjas musicales.

El campo `link` es opcional. Si se agrega, el programa queda clickeable en la grilla.

---

### `data/publicidades.json`

Define anunciantes/publicidades.

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

---

## Programas, episodios y audios

Cada programa vive dentro de:

```txt
content/programas/<slug_del_programa>/
```

Ejemplo:

```txt
content/programas/acha_y_machete/
  _index.md
  acha-y-machete-104/
    index.md
```

La página `_index.md` describe el programa. Cada episodio o publicación del programa es una carpeta con su propio `index.md`.

### Metadata de podcast del programa

Para que un programa tenga RSS de podcast completo, agregar en su `_index.md` un bloque `podcast`:

```yaml
---
title: "Acha y Machete"
description: "Programas de Acha y Machete en Radio San Javier."
podcast:
  author: "Acha y Machete"
  ownerName: "Radio San Javier"
  ownerEmail: "radiosanjavier@gmail.com"
  description: "Programas de Acha y Machete en Radio San Javier."
  category: "Society & Culture"
  explicit: "no"
  image: "https://archive.org/download/.../imagen.jpg"
---
```

El RSS del programa queda disponible en:

```txt
/programas/<slug_del_programa>/index.xml
```

Ejemplo:

```txt
/programas/acha_y_machete/index.xml
```

Ese RSS incluye tags para clientes genéricos y plataformas tipo Apple Podcasts, Spotify y YouTube Podcasts.

### Subir un episodio con audio

En el episodio, usar esta estructura:

```yaml
---
title: "Acha y Machete #104"
date: 2026-07-17T18:00:00-03:00
description: "Música de Bolivia. Programa emitido el 17/7/26."
rss_description: "Música de Bolivia. Programa emitido el 17/7/26."
draft: false
duration: "1:58:34"
image: "https://archive.org/download/acha-y-machete-104-17-7-26.mp-3_202607/BOLIVIA%20MUSICA.jpg"
archive:
  id: "acha-y-machete-104-17-7-26.mp-3_202607"
  url: "https://archive.org/details/acha-y-machete-104-17-7-26.mp-3_202607"
  image: "https://archive.org/download/acha-y-machete-104-17-7-26.mp-3_202607/BOLIVIA%20MUSICA.jpg"
audio:
  - "https://archive.org/download/acha-y-machete-104-17-7-26.mp-3_202607/ACHA%20Y%20MACHETE%20104%20-%2017-7-26.mp3.mp3"
enclosures:
  - url: "https://archive.org/download/acha-y-machete-104-17-7-26.mp-3_202607/ACHA%20Y%20MACHETE%20104%20-%2017-7-26.mp3.mp3"
    type: "audio/mpeg"
    length: 284549818
---

{{< archive-player id="acha-y-machete-104-17-7-26.mp-3_202607" >}}
```

Campos importantes:

- `description`: descripción visible del episodio.
- `rss_description`: descripción específica para RSS/podcast.
- `duration`: duración del audio. Formato recomendado: `HH:MM:SS` o `MM:SS`.
- `image`: imagen del episodio para OpenGraph y podcast.
- `archive.id`: identificador del item en Archive.org.
- `audio`: lista simple de URLs de audio. Debe ser una lista de strings para no romper metadata/OpenGraph del tema.
- `enclosures`: lista con metadata completa del audio para RSS.
  - `url`: URL directa al archivo de audio.
  - `type`: MIME type. Para mp3 usar `audio/mpeg`.
  - `length`: tamaño del archivo en bytes.

### Importante sobre `audio` y `enclosures`

No usar este formato en `audio`:

```yaml
audio:
  - url: "https://...mp3"
    type: "audio/mpeg"
    length: 123
```

El tema Blowfish espera que `audio` sea una lista de strings y puede fallar al generar OpenGraph.

Usar en cambio:

```yaml
audio:
  - "https://...mp3"
enclosures:
  - url: "https://...mp3"
    type: "audio/mpeg"
    length: 123
```

### Cómo obtener datos desde Archive.org

Para un item de Archive.org como:

```txt
https://archive.org/details/acha-y-machete-104-17-7-26.mp-3_202607
```

El ID es:

```txt
acha-y-machete-104-17-7-26.mp-3_202607
```

La metadata está en:

```txt
https://archive.org/metadata/acha-y-machete-104-17-7-26.mp-3_202607
```

Ahí se pueden ver:

- nombre exacto del `.mp3`;
- tamaño en bytes (`size`), para `enclosures.length`;
- duración (`length`), para calcular `duration`;
- imágenes disponibles.

### Reproductor de Archive.org

Para incrustar el reproductor de Archive.org dentro del episodio:

```md
{{< archive-player id="ID_DE_ARCHIVE" >}}
```

Ejemplo:

```md
{{< archive-player id="acha-y-machete-104-17-7-26.mp-3_202607" >}}
```
