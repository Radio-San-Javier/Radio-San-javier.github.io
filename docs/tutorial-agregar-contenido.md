# Tutorial para agregar contenido al sitio

Guía paso a paso para personas que no necesitan saber programar.

> Este tutorial usa el editor web del sitio, también llamado **Decap CMS**.

---

## 1. Entrar al editor

Abrí en el navegador:

```txt
https://radiosanjavier.netlify.app/admin/
```

Vas a ver la pantalla de acceso.

![Placeholder: captura de pantalla del login del editor](./images/01-login-editor.png)

Ingresá con tu usuario autorizado.

---

## 2. Qué se puede editar desde el editor

Desde el menú lateral vas a encontrar secciones como:

- **Noticias**
- **Páginas de programas**
- **Episodios - Acha y Machete**
- **Episodios - Es lo que hay**
- **Datos del sitio**

![Placeholder: captura del menú lateral del CMS](./images/02-menu-cms.png)

---

## 3. Agregar una noticia

Entrá a:

```txt
Noticias
```

Hacé click en:

```txt
New Noticias
```

o el botón equivalente para crear una noticia nueva.

![Placeholder: botón para crear noticia](./images/03-nueva-noticia.png)

Completá los campos:

- **Título**: nombre de la noticia.
- **Fecha**: fecha de publicación.
- **Descripción**: resumen breve.
- **Imagen principal**: imagen local opcional.
- **URL de imagen externa**: alternativa si la imagen ya está en internet.
- **Contenido**: texto principal de la noticia.
- **Borrador**: dejar activado si todavía no querés publicar.
- **Tags**: palabras clave opcionales.

![Placeholder: formulario de noticia](./images/04-formulario-noticia.png)

Cuando termines, guardá/publicá desde el botón del editor.

---

## 4. Editar la página de un programa

Entrá a:

```txt
Páginas de programas
```

Elegí el programa que querés modificar.

Por ejemplo:

```txt
Acha y Machete
```

![Placeholder: listado de páginas de programas](./images/05-programas.png)

Ahí podés editar:

- nombre del programa;
- descripción;
- imagen;
- texto de presentación;
- datos de podcast/RSS.

### Datos de podcast

La sección **Podcast / RSS** sirve para que el programa tenga un feed de podcast.

Campos importantes:

- **Autor**: nombre del programa.
- **Nombre propietario**: normalmente `Radio San Javier`.
- **Email propietario**: email de contacto.
- **Descripción podcast**: descripción que ven las apps de podcast.
- **Categoría**: por ejemplo `Society & Culture`.
- **Explícito**: normalmente `no`.
- **Imagen podcast**: URL de imagen para el podcast.

![Placeholder: campos podcast de programa](./images/06-podcast-programa.png)

> Para Apple Podcasts, Spotify y otras plataformas conviene usar una imagen cuadrada y grande.

---

## 5. Agregar un episodio de programa

Entrá a la colección del programa correspondiente.

Por ejemplo:

```txt
Episodios - Acha y Machete
```

Hacé click en crear nuevo episodio.

![Placeholder: crear episodio](./images/07-nuevo-episodio.png)

Completá los campos principales:

- **Título**: ejemplo `Acha y Machete #104`.
- **Fecha**: fecha de emisión o publicación.
- **Descripción**: resumen visible en la web.
- **Descripción para RSS**: resumen para apps de podcast.
- **Borrador**: activado si todavía no querés publicarlo.
- **Duración**: ejemplo `1:58:34`.
- **Imagen externa**: imagen del episodio.

![Placeholder: campos básicos de episodio](./images/08-formulario-episodio.png)

---

## 6. Agregar un episodio desde Archive.org

Muchos programas suben audios a Archive.org.

Ejemplo:

```txt
https://archive.org/details/acha-y-machete-104-17-7-26.mp-3_202607
```

El **ID de Archive.org** es la parte final de la URL:

```txt
acha-y-machete-104-17-7-26.mp-3_202607
```

### 6.1. Completar campos de Archive.org

En el episodio, buscá la sección:

```txt
Archive.org
```

Completá:

- **ID de Archive.org**: el ID del item.
- **URL de Archive.org**: la URL completa.
- **Imagen de Archive.org**: URL de imagen, si corresponde.

![Placeholder: campos Archive.org](./images/09-archive-fields.png)

---

## 7. Conseguir el link directo al MP3

Para que el episodio funcione como podcast, no alcanza con poner la página de Archive.org. Hay que usar el link directo al archivo `.mp3`.

Para encontrarlo, abrí esta URL:

```txt
https://archive.org/metadata/ID_DE_ARCHIVE
```

Ejemplo:

```txt
https://archive.org/metadata/acha-y-machete-104-17-7-26.mp-3_202607
```

Ahí vas a ver una lista de archivos.

Buscá el archivo que sea MP3.

Ejemplo:

```txt
ACHA Y MACHETE 104 - 17-7-26.mp3.mp3
```

La URL directa se arma así:

```txt
https://archive.org/download/ID_DE_ARCHIVE/NOMBRE_DEL_ARCHIVO.mp3
```

Ejemplo real:

```txt
https://archive.org/download/acha-y-machete-104-17-7-26.mp-3_202607/ACHA%20Y%20MACHETE%20104%20-%2017-7-26.mp3.mp3
```

![Placeholder: metadata de Archive.org mostrando archivos](./images/10-metadata-archive.png)

---

## 8. Completar Audio y Enclosures RSS

En el episodio hay dos secciones parecidas:

### Audio

Acá va solo la URL directa al MP3.

Ejemplo:

```txt
https://archive.org/download/acha-y-machete-104-17-7-26.mp-3_202607/ACHA%20Y%20MACHETE%20104%20-%2017-7-26.mp3.mp3
```

![Placeholder: campo Audio](./images/11-audio-url.png)

### Enclosures RSS

Esta sección sirve para que Apple Podcasts, Spotify, YouTube Podcasts y otros clientes lean bien el episodio.

Completá:

- **URL MP3**: la misma URL directa al MP3.
- **Tipo MIME**: para mp3 usar `audio/mpeg`.
- **Tamaño en bytes**: el tamaño del archivo. Sale de la metadata de Archive.org, campo `size`.

Ejemplo:

```txt
URL MP3: https://archive.org/download/.../archivo.mp3
Tipo MIME: audio/mpeg
Tamaño en bytes: 284549818
```

![Placeholder: campos Enclosures RSS](./images/12-enclosures.png)

---

## 9. Mostrar el reproductor de Archive.org dentro del episodio

En el campo **Contenido**, agregá esta línea:

```md
{{< archive-player id="ID_DE_ARCHIVE" >}}
```

Ejemplo:

```md
{{< archive-player id="acha-y-machete-104-17-7-26.mp-3_202607" >}}
```

Esto muestra el reproductor embebido de Archive.org en la página del episodio.

![Placeholder: contenido con shortcode archive-player](./images/13-shortcode-archive-player.png)

---

## 10. Publicar o guardar como borrador

Si el contenido todavía no está listo, activá:

```txt
Borrador
```

Si ya está listo para salir publicado, dejalo desactivado.

Después usá el botón de guardar/publicar del CMS.

![Placeholder: botón guardar/publicar](./images/14-publicar.png)

---

## 11. Revisar el resultado

Después de publicar, revisar:

### Página del episodio

```txt
https://radiosanjavier.netlify.app/programas/acha_y_machete/acha-y-machete-104/
```

### RSS del programa

```txt
https://radiosanjavier.netlify.app/programas/acha_y_machete/index.xml
```

En el RSS debería aparecer algo como:

```xml
<enclosure url="https://archive.org/download/.../archivo.mp3" length="284549818" type="audio/mpeg"/>
```

Ese `enclosure` es lo que necesitan las apps de podcast.

---

## 12. Editar datos generales del sitio

Entrá a:

```txt
Datos del sitio
```

Ahí podés editar:

### Radio / Streaming

Sirve para cambiar:

- nombre de la radio;
- frecuencia;
- bajada;
- URL del streaming en vivo.

![Placeholder: datos de radio](./images/15-datos-radio.png)

### Publicidades

Sirve para agregar o desactivar anunciantes.

Campos:

- nombre;
- imagen;
- link;
- activo;
- ubicaciones.

Las imágenes de publicidades deberían subirse/guardarse en:

```txt
static/publicidades/
```

En el editor o en `data/publicidades.json`, la ruta se escribe sin `static`:

```txt
/publicidades/nombre-del-archivo.svg
```

Ejemplos válidos:

```txt
/publicidades/almacen-don-pepe.svg
/publicidades/almacen-don-pepe.png
/publicidades/farmacia-central.webp
```

![Placeholder: datos de publicidades](./images/16-publicidades.png)

---

## 13. Ubicaciones de publicidades

Las ubicaciones indican dónde aparece una publicidad.

Ejemplos:

```txt
home
es_lo_que_hay
acha_y_machete
```

Si una publicidad tiene:

```txt
home
```

aparece en la página principal.

Si tiene:

```txt
es_lo_que_hay
```

aparece en páginas asociadas a ese programa.

---

## 14. Checklist antes de publicar un episodio

Antes de publicar, revisar:

- [ ] El título está bien escrito.
- [ ] La fecha es correcta.
- [ ] La descripción está completa.
- [ ] La duración está cargada.
- [ ] La imagen funciona.
- [ ] El ID de Archive.org es correcto.
- [ ] La URL directa al MP3 abre en el navegador.
- [ ] El `enclosure` tiene tipo `audio/mpeg`.
- [ ] El tamaño en bytes está cargado.
- [ ] El reproductor de Archive.org aparece en el contenido.
- [ ] El episodio no está como borrador si debe publicarse.

---

## 15. Si algo sale mal

### No aparece el episodio

Revisar:

- que no esté marcado como borrador;
- que esté dentro de la colección correcta;
- que tenga fecha válida.

### El reproductor no aparece

Revisar que el contenido tenga:

```md
{{< archive-player id="ID_DE_ARCHIVE" >}}
```

### El podcast no reproduce

Revisar:

- que la URL directa al MP3 funcione;
- que `Enclosures RSS` tenga URL, tipo y tamaño;
- que el tipo MIME sea `audio/mpeg`.

### La imagen no aparece en apps de podcast

Puede ser por tamaño o formato. Para plataformas grandes conviene usar una imagen cuadrada grande, idealmente 1400x1400 o más.
