# Context: Catálogo AR — Alfredo Ravelo (Acuarelas)

## Qué es esto
Sitio web estático de catálogo de obras de arte (acuarelas) del artista Alfredo Ravelo. Funciona como galería + vitrina de ventas. No tiene backend — todo es HTML/CSS/JS vanilla + un archivo JSON.

## Stack actual
- HTML/CSS/JS vanilla (sin frameworks)
- Bootstrap 5 en `index.html` (solo grid/navbar — se elimina en Sprint 6)
- `obras.json` — fuente de verdad de todas las obras
- Archivos estáticos, deployable en Netlify, GitHub Pages, etc.

## Estructura de archivos
```
/
├── index.html          # Galería principal — AÚN ~1400 líneas hardcodeadas (refactorizar Sprint 6)
├── styles.css          # Estilos globales
├── obras.json          # Fuente de verdad: id, title, image, measures, technique, description, award
├── preview.html        # AR viewer (COMPLETO — Sprint 5b)
├── info.html           # Detalle de obra (?id= por query string)
├── size.html           # Comparador de tamaños
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

## Tamaños disponibles
| data-size | Medidas |
|-----------|---------|
| media     | 35×50 cm |
| hoja      | 50×70 cm |
| 2hojas    | 65×100 cm |
| 3hojas    | 85×200 cm |
| 4hojas    | 110×150 cm |

---

## Estado de sprints

### Fase 1 — AR viewer (preview.html) COMPLETA ✅

**Sprint 1–5b completados.** preview.html es un AR viewer funcional con:
- Cámara trasera (getUserMedia), overlay de pintura draggable
- Pinch-zoom con dos dedos + slider horizontal
- Dos métodos de calibración de escala real:
  - **A4**: marco visual — pintura se oculta, usuario ajusta slider al tamaño de una hoja A4 real
  - **10cm**: toca dos puntos en la pared separados 10 cm exactos
- Calibración persiste en localStorage entre sesiones
- Panel inferior colapsable (52px siempre visible) — se colapsa automáticamente al seleccionar pintura
- Categorías como pills scrolleables generadas dinámicamente desde obras.json
- Thumbnails con barra de tamaño proporcional al área real de la obra
- Marco de cuadro realista (CSS pseudo-elements): café oscuro con passepartout crema
- Screenshot via canvas compositing (frame de video + marco + imagen)
- Orientación detectada por foto: asigna dimensión declarada correctamente
- Paleta: negro + blanco puro, tipografía light, estética museo

**Decisiones de diseño AR cerradas:**
- Sin PWA, sin modo comparar, sin ajuste de brillo (eliminados por decisión)
- Sin html2canvas — screenshot propio con canvas API
- Escala siempre fija calibrada por usuario, no auto-escala por distancia

### Fase 2 — Refactorización galería ← SIGUIENTE

- **Sprint 6** ← EN PLANEACIÓN
- **Sprint 7** Performance de imágenes (WebP, lazy, blur-up)

---

## Problemas conocidos en index.html (pendientes Sprint 6)
1. ~1400 líneas hardcodeadas — no usa obras.json
2. Sin `loading="lazy"` en imágenes
3. Imágenes JPG sin comprimir (~3–8 MB cada una)
4. Typo: "50x 70 com" (en filtro de tamaño)
5. Sin conexión galería → AR: usuario debe buscar la pintura de nuevo en preview.html
6. Paleta inconsistente: index.html usa amarillo (#ffc107), preview.html usa blanco

## Notas de UX
- Interfaz en español. Artista y mercado mexicano.
- Usuarios: coleccionistas/compradores.
- AR es el diferenciador clave. Flujo galería → AR debe ser sin fricción.
- Mobile-first.
- Estética: galería de arte / museo. Negro + blanco. Sin decoración innecesaria.
