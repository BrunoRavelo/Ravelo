# Context: Catálogo AR — Alfredo Ravelo (Acuarelas)

## Qué es esto
Sitio web estático de catálogo de obras de arte (acuarelas) del artista Alfredo Ravelo. Funciona como galería + vitrina de ventas. No tiene backend — todo es HTML/CSS/JS vanilla + un archivo JSON.

## Stack actual
- HTML/CSS/JS vanilla sin frameworks (Bootstrap 5 solo en `info.html` para grid)
- `obras.json` — única fuente de verdad para todas las obras
- Archivos estáticos, deployable en Netlify, GitHub Pages, XAMPP local, etc.

## Estructura de archivos
```
/
├── index.html          # Galería principal — reescrita completamente, carga desde obras.json
├── info.html           # Detalle de obra (?id= por query string)
├── preview.html        # AR viewer completo
├── size.html           # Comparador de tamaños
├── obras.json          # Fuente de verdad: id, title, image, measures, technique, description, award
├── styles.css          # Estilos globales (poco usado — estilos viven en cada HTML)
└── assets/
    ├── logo.png
    ├── flores/ rostros/ desnudos/ catrinas/ paisajes/ expresiones/
    ├── mexico/ naturalezamuerta/ sacro/ payasos/ celebridades/ manos/ animales/
```

## obras.json — formato
```json
{
  "id": 1,
  "title": "Sinfonía de Flores",
  "image": "assets/flores/flores1.jpg",
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

Reescrito completamente. Sin Bootstrap. Carga 100% desde `obras.json`.

**Diseño:**
- Fondo negro, tipografía light, estética galería/museo
- Navbar sticky: logo (`assets/logo.png`) + texto "Alfredo Ravelo" (texto oculto en móvil ≤540px, logo siempre visible) + "Guía de Tamaños" + "Ver en pared" (sin borde/marco)
- Filter bar sticky debajo del navbar: pill de categoría + pill de tamaño
- Galería CSS Grid de 12 columnas
- Footer: "© Alfredo Ravelo. Todos los derechos reservados"

**Márgenes y responsividad:**
- `--px: clamp(16px, 8vw, 160px)` — márgenes laterales fluidos (amplios en desktop, angostos en móvil)
- `--gap: 18px` desktop / `12px` móvil — separación entre pinturas
- `max-width: 1600px` centrado en galería

**Grilla de pinturas:**
- `gi-large` → span 6 (50%) | desktop
- `gi-medium` → span 4 (33%)
- `gi-small` → span 3 (25%)
- ≤900px: large=12, medium=6, small=6
- ≤540px: **todas → span 12** (una pintura por fila, ancho completo)
- `LARGE_IDS` — Set de IDs con layout curado (replicando distribución del index anterior)
- Fallback automático por área para obras no listadas en LARGE_IDS

**Interacción:**
- **Desktop** (`pointer: fine`): hover sobre pintura → overlay con "Ampliar" (abre lightbox) e "Información" (navega a info.html)
- **Móvil** (`pointer: coarse`): tap en pintura → navega a info.html
- Lightbox full-screen con navegación por flechas y teclado (←→ Esc)
- Overlay oculto en móvil vía `@media (pointer: coarse)`

**Filtros:**
- Categorías generadas dinámicamente desde obras.json con conteo
- Conteo de categorías se actualiza al cambiar filtro de tamaño
- Filtros de tamaño: Todos / Pequeño (35×50) / Mediano (50×70) / Grande (65×100) / Muy grande (85–110 cm)
- Estado de filtros persiste en `localStorage` (keys: `filter_cat`, `filter_size`)
- Posición de scroll persiste en `sessionStorage` (key: `scroll_pos`) — se restaura al volver de info.html

**Skeleton loading:**
- 14 tarjetas skeleton con shimmer aparecen mientras carga obras.json
- Se reemplazan con tarjetas reales al terminar el fetch
- Imágenes usan `loading="lazy"` y fondo `#111` como placeholder

**Overlay de instrucciones (primera visita):**
- Aparece una sola vez (localStorage key: `ar_intro_seen`)
- Muestra logo + "Alfredo Ravelo" + mensaje según dispositivo:
  - Desktop: "Desliza el mouse encima de la pintura para expandir o ver su información."
  - Móvil: "Toca una pintura para ver su información o proyectarla en tu pared con realidad aumentada."
- Detecta dispositivo con `window.matchMedia('(pointer: fine)')`

**Scroll to top:**
- Botón circular fijo en esquina inferior derecha, aparece tras 300px de scroll

---

### info.html — COMPLETO ✅

Página de detalle de obra. Usa Bootstrap 5 solo para grid de columna centrada.

**Layout:**
- Navbar fijo en la parte superior: botón "← Volver" (navega a index.html)
- Contenido centrado verticalmente en el viewport (`min-height: 100dvh`, `justify-content: center`)
- Scroll habilitado como tolerancia para pantallas pequeñas o descripciones largas

**Imagen:**
- `max-height: clamp(160px, 32vh, 300px)` — imagen pequeña, no protagonista
- Orientación detectada por `naturalHeight vs naturalWidth`:
  - Vertical → `col-sm-10 col-md-6 col-lg-4`
  - Horizontal → `col-sm-10 col-md-8 col-lg-6`
- `border-radius: 6px`

**Texto:**
- Título: `clamp(15px, 2.2vw, 20px)`
- Párrafos (medidas, técnica, descripción, premio): `clamp(12px, 1.5vw, 14px)`
- Color: `rgba(255,255,255,0.80)`

**Botón AR:**
- "Ver en pared. Realidad Aumentada"
- Guarda `ar_preselect` en localStorage con el ID de la obra
- Redirige a `preview.html`

---

### preview.html — COMPLETO ✅

AR viewer funcional. Ver detalle en sección siguiente.

**Pantalla de bienvenida:**
- Logo `assets/logo.png` arriba + título "Ver en tu pared"
- Botón "Activar cámara"

**Spinner de carga de pintura:**
- Spinner centrado aparece mientras `paintImg` carga al seleccionar una obra
- Desaparece en `onload` / `onerror`

**Flujo desde info.html:**
- Lee `localStorage.getItem('ar_preselect')` al iniciar
- Si existe, selecciona esa obra automáticamente y va directo al AR (sin mostrar instrucciones)

---

### preview.html — Funcionalidades AR detalladas

- Cámara trasera (`getUserMedia`), overlay de pintura draggable
- Pinch-zoom con dos dedos + slider horizontal
- Marco de cuadro CSS: café oscuro con passepartout crema
- Dos métodos de calibración de escala real:
  - **A4**: marco visual ajustable al tamaño de una hoja A4 real
  - **10cm**: toca dos puntos en la pared separados 10 cm exactos
- Calibración persiste en `localStorage`
- Panel inferior colapsable (52px siempre visible)
- Categorías como pills scrolleables desde obras.json
- Thumbnails con barra proporcional al área real
- Screenshot: canvas compositing (video + marco + imagen)
- Status pills para feedback al usuario
- Textos: sin guiones largos (—), se usan punto y coma

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
