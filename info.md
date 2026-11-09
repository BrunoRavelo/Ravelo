# Context: Catálogo AR — Alfredo Ravelo (Acuarelas)

## Qué es esto
Sitio web estático de catálogo de obras de arte (acuarelas) del artista Alfredo Ravelo. Funciona como galería + vitrina de ventas. No tiene backend — todo es HTML/CSS/JS vanilla + un archivo JSON.

## Stack actual
- HTML/CSS/JS vanilla sin frameworks (Bootstrap 5 solo en `info.html` y `size.html` para grid).
- `obras.json` — única fuente de verdad para todas las obras.
- Archivos estáticos, deployable en Netlify, GitHub Pages, XAMPP local, etc.
- **Imágenes en formato WebP** (carpeta `assetswebp/`) para garantizar la mejor carga y rendimiento en la galería.

## Estructura de archivos
```
/
├── index.html          # Galería principal — carga desde obras.json
├── info.html           # Detalle de obra (?id= por query string)
├── preview.html        # AR viewer completo (realidad aumentada)
├── size.html           # Comparador visual de tamaños (sillón)
├── obras.json          # Fuente de verdad: id, title, image, measures, technique, description, award
├── convert_webp.py     # Script de Python para convertir imágenes a WebP
├── styles.css          # Estilos globales legacy (la mayoría de estilos viven en cada HTML)
└── assetswebp/
    ├── logo.webp
    ├── sofa.svg
    ├── flores/ rostros/ desnudos/ catrinas/ paisajes/ expresiones/
    ├── mexico/ naturalezamuerta/ sacro/ payasos/ celebridades/ manos/ animales/
```

---

## Script de Conversión (`convert_webp.py`)

Para mantener el sitio rápido, **las imágenes deben estar en formato WebP**. El archivo `convert_webp.py` automatiza esta tarea.

**¿Cómo funciona?**
1. El script lee el archivo `obras.json` para saber qué imágenes se están utilizando realmente.
2. Busca los archivos originales (JPG, PNG, etc.) dentro de la carpeta `assets/` (que actúa como fuente original y no es modificada).
3. Convierte cada imagen a formato `.webp` con una calidad optimizada (82) y las guarda en la carpeta `assetswebp/`, manteniendo la misma estructura de subcarpetas.
4. También convierte imágenes "huérfanas" (que están en `assets/` pero no se usan en `obras.json`, como el logo o el sillón).
5. Genera un reporte llamado `info_conversion.md` que detalla cuánto peso se ahorró y si hubo errores o imágenes faltantes.

*Para ejecutarlo, se requiere tener Python y la librería Pillow instalados (`pip install Pillow`).*

---

## obras.json — formato
```json
{
  "id": 1,
  "title": "Sinfonía de Flores",
  "image": "assetswebp/flores/flores1.webp",
  "measures": "110 x 150 cm",
  "technique": "Acuarela sobre papel de algodón",
  "description": "...",
  "award": ""
}
```

**Convención de medidas — CRÍTICO:**
Las medidas SIEMPRE van del número menor al mayor, sin importar orientación real.
"50 x 70 cm" puede ser vertical u horizontal — la foto determina cuál es cuál.
- Foto horizontal (naturalWidth > naturalHeight) → número grande = ancho, chico = alto.
- Foto vertical   (naturalHeight > naturalWidth) → número grande = alto, chico = ancho.
La categoría se infiere del path de la imagen (ej. `/flores/` → "flores").

## Tamaños disponibles (obras.json)
| Clave    | Medidas      |
|----------|--------------|
| media    | 35 × 50 cm   |
| hoja     | 50 × 70 cm   |
| 2hojas   | 65 × 100 cm  |
| 3hojas   | 85 × 200 cm  |
| 4hojas   | 110 × 150 cm |

---

## Estado actual de cada archivo

### index.html — COMPLETO ✅

Reescrito completamente. Sin Bootstrap. Carga 100% desde `obras.json` y usa las imágenes optimizadas de `assetswebp/`.

**Diseño:**
- Fondo negro, tipografía light, estética galería/museo.
- Navbar sticky: logo (`assetswebp/logo.webp`) + texto "Alfredo Ravelo" (texto oculto en móvil ≤540px, logo siempre visible) + "Guía de Tamaños" + "Ver en pared" (sin borde/marco).
- Filter bar sticky debajo del navbar: pill de categoría + pill de tamaño.
- Galería CSS Grid de 12 columnas.
- Footer: "© Alfredo Ravelo. Todos los derechos reservados".

**Márgenes y responsividad:**
- `--px: clamp(16px, 8vw, 160px)` — márgenes laterales fluidos.
- `--gap: 18px` desktop / `12px` móvil.
- `max-width: 1600px` centrado en galería.

**Grilla de pinturas:**
- `gi-large` → span 6 (50%) | desktop.
- `gi-medium` → span 4 (33%).
- `gi-small` → span 3 (25%).
- ≤900px: large=12, medium=6, small=6.
- ≤540px: **todas → span 12** (una pintura por fila).
- `LARGE_IDS` — Set de IDs con layout curado.
- Fallback automático por área para obras no listadas en LARGE_IDS.

**Interacción:**
- **Desktop** (`pointer: fine`): hover sobre pintura → overlay con "Ampliar" (lightbox) e "Información" (info.html).
- **Móvil** (`pointer: coarse`): tap en pintura → navega a info.html.
- Lightbox full-screen con navegación por flechas y teclado (←→ Esc).
- Overlay oculto en móvil vía `@media (pointer: coarse)`.

**Filtros:**
- Categorías generadas dinámicamente desde obras.json con conteo.
- Conteo de categorías se actualiza al cambiar filtro de tamaño.
- Filtros de tamaño: Todos / Pequeño (35×50) / Mediano (50×70) / Grande (65×100) / Muy grande (85–110 cm).
- Estado de filtros persiste en `localStorage` (keys: `filter_cat`, `filter_size`).
- Posición de scroll persiste en `sessionStorage` (key: `scroll_pos`).

**Skeleton loading:**
- 14 tarjetas skeleton con shimmer aparecen mientras carga obras.json.
- Imágenes usan `loading="lazy"` y fondo `#111` como placeholder.

**Overlay de instrucciones (primera visita):**
- Aparece una sola vez (localStorage key: `ar_intro_seen`).
- Detecta dispositivo con `window.matchMedia('(pointer: fine)')` para mostrar el mensaje adecuado.

**Scroll to top:**
- Botón circular fijo en esquina inferior derecha, aparece tras 300px de scroll.

---

### info.html — COMPLETO ✅

Página de detalle de obra. Usa Bootstrap 5 solo para grid de columna centrada.

**Layout:**
- Navbar fijo en la parte superior: botón "← Volver".
- Contenido centrado verticalmente en el viewport (`min-height: 100dvh`, `justify-content: center`).
- Scroll habilitado como tolerancia.

**Imagen:**
- `max-height: clamp(160px, 32vh, 300px)` — imagen pequeña, no protagonista.
- Orientación detectada por `naturalHeight vs naturalWidth`:
  - Vertical → `col-sm-10 col-md-6 col-lg-4`
  - Horizontal → `col-sm-10 col-md-8 col-lg-6`
- `border-radius: 6px`.

**Texto:**
- Título: `clamp(15px, 2.2vw, 20px)`.
- Párrafos (medidas, técnica, descripción, premio): `clamp(12px, 1.5vw, 14px)`.

**Botón AR:**
- "Ver en pared. Realidad Aumentada".
- Guarda `ar_preselect` en localStorage con el ID de la obra y redirige a `preview.html`.

---

### preview.html — COMPLETO ✅

AR viewer funcional.

**Pantalla de bienvenida:**
- Logo `assetswebp/logo.webp` arriba + título "Ver en tu pared" + botón "Activar cámara".

**Flujo desde info.html:**
- Lee `localStorage.getItem('ar_preselect')`. Si existe, selecciona la obra automáticamente y va directo al AR.

**Funcionalidades AR detalladas:**
- Cámara trasera (`getUserMedia`), overlay de pintura draggable.
- Pinch-zoom con dos dedos + slider horizontal.
- Marco de cuadro CSS: café oscuro con passepartout crema.
- Dos métodos de calibración de escala real:
  - **A4**: marco visual ajustable al tamaño de una hoja A4 real.
  - **10cm**: toca dos puntos en la pared separados 10 cm exactos.
- Calibración persiste en `localStorage`.
- Panel inferior colapsable (52px siempre visible).
- Categorías como pills scrolleables desde obras.json.
- Thumbnails con barra proporcional al área real.
- Screenshot: canvas compositing (video + marco + imagen).
- Status pills para feedback al usuario.

---

### size.html — COMPLETO ✅

Página de comparación visual de tamaños. Usa Bootstrap 5.

- Muestra un sillón SVG (`assetswebp/sofa.svg`) como referencia de escala.
- Botones con las medidas estándar (Media hoja, 1 hoja, 2 hojas, etc.).
- Al hacer clic, dibuja un rectángulo blanco con las proporciones exactas de la pintura al lado del sillón.
- El tamaño del sillón y los rectángulos se ajustan dinámicamente (`resizeElements`) dependiendo del ancho de la pantalla (celular, tablet, desktop).

---

## Paleta y convenciones visuales
- Fondo: `#000`
- Texto: `#fff` (principal) / `rgba(255,255,255,0.72)` (secundario) / `rgba(255,255,255,0.50)` (tenue)
- Bordes: `rgba(255,255,255,0.07)`
- Sin guiones largos (—) en texto visible al usuario. Usar punto (.) o coma (,).
- Sin emojis. Interfaz en español. Mercado mexicano.
- Estética: galería de arte / museo. Negro + blanco. Sin decoración innecesaria.

## Notas de UX
- Usuarios: coleccionistas/compradores.
- AR es el diferenciador clave. Flujo galería → info → AR debe ser sin fricción.
- Mobile-first. Detección de dispositivo vía `pointer: coarse` (móvil) / `pointer: fine` (desktop).
- Al volver de info.html a index.html: filtros y posición de scroll se restauran automáticamente.