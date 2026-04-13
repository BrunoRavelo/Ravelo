# Context: Catálogo AR — Alfredo Ravelo (Acuarelas)

## Qué es esto
Sitio web estático de catálogo de obras de arte (acuarelas) del artista Alfredo Ravelo. Funciona como galería + vitrina de ventas. No tiene backend ni base de datos — todo es HTML/CSS/JS vanilla + Bootstrap 5 + un archivo JSON de obras.

## Stack actual
- HTML/CSS/JS vanilla (sin frameworks)
- Bootstrap 5 (solo para grid y algunos componentes)
- `obras.json` — fuente de verdad de todas las obras
- Archivos estáticos, se puede servir desde cualquier hosting (Netlify, GitHub Pages, etc.)

## Estructura de archivos
```
/
├── index.html          # Galería principal (actualmente ~1400 líneas, hardcodeado)
├── styles.css          # Estilos globales
├── obras.json          # Fuente de verdad: todas las obras con título, medidas, técnica, descripción
├── preview.html        # ← PESTAÑA AR (Sprint 1: construida en este sprint)
├── info.html           # Detalle de una obra (recibe ?id= por query string)
├── size.html           # Comparador de tamaños
└── assets/
    ├── logo.png
    ├── flores/         # flores1.jpg, flores2.jpg, ...
    ├── rostros/        # rostro1.jpg, ...
    ├── catrinas/
    ├── desnudos/
    ├── paisajes/
    ├── expresiones/
    ├── mexico/
    ├── naturalezamuerta/
    ├── sacro/
    ├── payasos/
    ├── celebridades/
    ├── manos/
    └── animales/
```

## obras.json — formato de cada objeto
```json
{
  "id": 1,
  "title": "Sinfonía de Flores",
  "image": "assets/flores/flores1.jpg",   // ruta relativa desde root
  "measures": "110 x 150 cm",             // siempre "W x H cm"
  "technique": "Acuarela sobre papel de algodón",
  "description": "...",
  "award": ""                              // vacío si no tiene premio
}
```

## Tamaños disponibles (data-size en HTML)
| data-size | Medidas reales |
|-----------|----------------|
| media     | 35 × 50 cm     |
| hoja      | 50 × 70 cm     |
| 2hojas    | 65 × 100 cm    |
| 3hojas    | 85 × 200 cm    |
| 4hojas    | 110 × 150 cm   |

## Categorías disponibles (data-category)
flores, celebridades, catrinas, payasos, sacro, mexico, desnudos, rostros, animales, expresion, manos, paisaje, nat

## Variables CSS (styles.css)
```css
--main-bg-color: #000
--secondary-bg-color: #111
--hover-bg-color: #333
--light-text-color: #fff
--highlight-color: #ffc107       /* dorado — color de acento principal */
--transparent-grey: rgba(128,128,128,0.5)
```

---

## Roadmap de sprints

### Fase 1 — AR (vanilla JS, sin librerías AR)
- **Sprint 1 ✅** `preview.html`: cámara (getUserMedia), overlay de pintura draggable, pinch-to-zoom, slider de escala, calibración A4 (marco amarillo de referencia), thumbnails de obras desde datos inline, instrucciones al primer uso.
- **Sprint 2** `preview.html` mejora: fetch desde `obras.json`, calibración de 2 puntos (más precisa), selector por categoría, indicador de dimensiones en pantalla, guardar última escala calibrada en localStorage.
- **Sprint 3** `preview.html` polish: sombra realista de cuadro, modo screenshot (html2canvas), comparar 2 pinturas, ajuste de brillo de pared (filtro CSS), tour de instrucciones animado.

### Fase 2 — Refactorización galería
- **Sprint 4**: Reemplazar `index.html` hardcodeado por galería dinámica (fetch `obras.json` → renderizar tarjetas). El HTML de la galería queda en ~50 líneas. Mantener mismos filtros y comportamiento.
- **Sprint 5**: UI mejorada — pills horizontales de categoría (siempre visibles, reemplaza dropdown), sidebar sticky de filtros en desktop, layout masonry real (cada columna tiene sus proporciones de pintura), transiciones CSS al filtrar.

### Fase 3 — Performance de imágenes
- **Sprint 6**: Script Node.js (Sharp) para convertir todos los JPG a WebP + generar thumbnails 40px para blur placeholder. Agregar `loading="lazy"` + Intersection Observer + técnica de blur-up (imagen tiny → imagen real con transición). Preload solo categoría visible.

---

## Decisiones de diseño ya tomadas
1. **Escala AR**: tamaño fijo calibrado por usuario (no auto-escala por distancia). Calibración mediante hoja A4 como referencia física.
2. **Sin librerías AR** en Fase 1 — solo getUserMedia + CSS transforms. MindAR.js se evalúa para Sprint futuro (Fase 2 del AR).
3. **Proporciones**: parsear `measures` del JSON para calcular px proporcionales a cm. Una pintura de 110×150 debe verse siempre más grande que una de 35×50.
4. **Sin backend**: todo es estático. Si en el futuro se necesita carrito o auth, evaluar Next.js.
5. **Colores**: negro + dorado (#ffc107) — estética de galería de arte. No cambiar la paleta principal.

---

## Problemas conocidos del código actual
1. `index.html` tiene ~1400 líneas de HTML duplicado — la galería está hardcodeada aunque existe `obras.json`. (Se arregla en Sprint 4)
2. Las imágenes no tienen `loading="lazy"` — todas cargan al mismo tiempo. (Sprint 6)
3. Las imágenes son JPG sin optimizar, probablemente 3–8 MB cada una. (Sprint 6)
4. El filtro de tamaño tiene un typo: "50x 70 com" (debería ser "50 × 70 cm").
5. `data-size="3hojas"` en el HTML corresponde a 85×200 pero el JSON dice `"measures": "85 x 200 cm"` — consistente, solo hay que saberlo.

## Notas de UX importantes
- El artista es mexicano — la interfaz está en español.
- Los usuarios principales son coleccionistas/compradores, no desarrolladores.
- La feature AR es el diferenciador clave — el cliente quiere saber cómo se ve la pintura en su pared ANTES de comprar.
- Mobile-first: la mayoría del tráfico esperado es desde celular.
