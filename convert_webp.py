#!/usr/bin/env python3
"""
convert_webp.py
---------------
Convierte las imagenes de assets/ a formato WebP y las guarda en assetswebp/
manteniendo la misma estructura de subcarpetas.

No modifica ni borra assets/ (los JPG originales se conservan).
Genera info_conversion.md con el reporte de conversion y las imagenes faltantes.

Uso:
    python convert_webp.py

Coloca este script en la raiz del proyecto (junto a obras.json).
"""

import os
import json

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow no esta instalado.")
    print("Activa tu venv y ejecuta:  pip install Pillow")
    raise SystemExit(1)

# ── Configuracion ──────────────────────────────────────────────
QUALITY = 82          # 80-85 es el punto dulce para arte (alta fidelidad, bajo peso)
METHOD  = 6           # 0=rapido, 6=mejor compresion (tarda un poco mas)
# ───────────────────────────────────────────────────────────────


def asset_key(path):
    """Clave de comparacion: subcarpeta/nombre_sin_extension en minusculas.
    Funciona con cualquier prefijo (assets/ o assetswebp/) y cualquier extension."""
    for prefix in ("assetswebp/", "assets/"):
        if path.startswith(prefix):
            path = path[len(prefix):]
            break
    return os.path.splitext(path)[0].lower().replace(os.sep, "/")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "assets")
    webp_dir   = os.path.join(script_dir, "assetswebp")
    obras_json = os.path.join(script_dir, "obras.json")

    print(f"Proyecto : {script_dir}")
    print(f"Origen   : {assets_dir}")
    print(f"Destino  : {webp_dir}")
    print(f"Calidad  : {QUALITY}\n")

    # ── Cargar obras.json ──────────────────────────────────────
    with open(obras_json, "r", encoding="utf-8") as f:
        obras = json.load(f)

    # ── Descubrir TODOS los archivos de imagen en assets/ ──────
    # Mapeo: clave_normalizada -> ruta_relativa
    # Ej: "flores/flores1" -> "assets/flores/flores1.JPG"
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}
    all_assets = {}
    for root, _, files in os.walk(assets_dir):
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext in image_extensions:
                full = os.path.join(root, fname)
                rel  = os.path.relpath(full, script_dir).replace(os.sep, "/")
                key  = asset_key(rel)
                all_assets[key] = rel

    referenced_keys = set()
    missing    = []
    converted  = []
    errors     = []
    total_orig = 0
    total_webp = 0

    # ── Procesar cada obra ─────────────────────────────────────
    print("Convirtiendo imagenes...")
    print("-" * 60)

    for obra in obras:
        oid      = obra.get("id", "?")
        title    = obra.get("title", "")
        img_path = obra.get("image", "").strip()  # puede ser assets/ o assetswebp/

        if not img_path:
            missing.append({
                "id": oid, "title": title,
                "path": "",
                "reason": "Sin campo 'image' en obras.json"
            })
            print(f"  ⚠  [{oid}] {title} — sin campo image")
            continue

        key = asset_key(img_path)
        referenced_keys.add(key)

        # Buscar el archivo original en assets/ usando la clave normalizada
        src_rel = all_assets.get(key)
        if src_rel is None:
            missing.append({
                "id": oid, "title": title,
                "path": img_path,
                "reason": "Archivo no encontrado en disco (assets/)"
            })
            print(f"  ✗  [{oid}] {img_path} — NO ENCONTRADO en assets/")
            continue

        src_path = os.path.join(script_dir, src_rel.replace("/", os.sep))

        # Destino: siempre assetswebp/subcarpeta/nombre.webp
        webp_rel  = key + ".webp"                                        # "flores/flores1.webp"
        dst_path  = os.path.join(webp_dir, webp_rel.replace("/", os.sep))
        webp_path = "assetswebp/" + webp_rel

        os.makedirs(os.path.dirname(dst_path), exist_ok=True)

        try:
            orig_size = os.path.getsize(src_path)

            with Image.open(src_path) as img:
                if img.mode in ("P", "LA"):
                    img = img.convert("RGBA")
                elif img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGB")
                img.save(dst_path, "WEBP", quality=QUALITY, method=METHOD)

            webp_size = os.path.getsize(dst_path)
            reduction = round((1 - webp_size / orig_size) * 100, 1)
            total_orig += orig_size
            total_webp += webp_size

            converted.append({
                "id"       : oid,
                "title"    : title,
                "orig_path": src_rel,
                "webp_path": webp_path,
                "orig_kb"  : orig_size  // 1024,
                "webp_kb"  : webp_size  // 1024,
                "reduction": reduction,
            })
            print(f"  ✓  [{oid}] {os.path.basename(src_path):30s}  "
                  f"{orig_size//1024:>5} KB  →  {webp_size//1024:>4} KB  ({reduction}%)")

        except Exception as exc:
            errors.append({
                "id": oid, "title": title,
                "path": img_path, "error": str(exc)
            })
            print(f"  ✗  [{oid}] {img_path} — ERROR: {exc}")

    # ── Huerfanas: en assets/ pero no referenciadas por obras.json ──
    orphan_keys       = sorted(set(all_assets.keys()) - referenced_keys)
    orphans_converted = []
    orphans_errors    = []

    if orphan_keys:
        print("\nConvirtiendo huerfanas...")
        print("-" * 60)

    for key in orphan_keys:
        rel_path  = all_assets[key]                                      # "assets/logo.png"
        src_path  = os.path.join(script_dir, rel_path.replace("/", os.sep))
        webp_rel  = key + ".webp"                                        # "logo.webp"
        dst_path  = os.path.join(webp_dir, webp_rel.replace("/", os.sep))
        webp_path = "assetswebp/" + webp_rel

        os.makedirs(os.path.dirname(dst_path), exist_ok=True)

        try:
            orig_size = os.path.getsize(src_path)

            with Image.open(src_path) as img:
                if img.mode in ("P", "LA"):
                    img = img.convert("RGBA")
                elif img.mode not in ("RGB", "RGBA"):
                    img = img.convert("RGB")
                img.save(dst_path, "WEBP", quality=QUALITY, method=METHOD)

            webp_size = os.path.getsize(dst_path)
            reduction = round((1 - webp_size / orig_size) * 100, 1)
            total_orig += orig_size
            total_webp += webp_size

            orphans_converted.append({
                "orig_path": rel_path,
                "webp_path": webp_path,
                "orig_kb"  : orig_size  // 1024,
                "webp_kb"  : webp_size  // 1024,
                "reduction": reduction,
            })
            print(f"  ✓  {os.path.basename(src_path):30s}  "
                  f"{orig_size//1024:>5} KB  →  {webp_size//1024:>4} KB  ({reduction}%)")

        except Exception as exc:
            orphans_errors.append({"path": rel_path, "error": str(exc)})
            print(f"  ✗  {rel_path} — ERROR: {exc}")

    # ── Escribir reporte ───────────────────────────────────────
    print("\n" + "-" * 60)
    print("Generando reporte...")

    report_path = os.path.join(script_dir, "info_conversion.md")
    orig_mb = total_orig / 1024 / 1024
    webp_mb = total_webp / 1024 / 1024
    total_reduction = round((1 - total_webp / total_orig) * 100, 1) if total_orig else 0

    with open(report_path, "w", encoding="utf-8") as f:

        f.write("# Reporte de conversion WebP\n\n")
        f.write(f"- **Imagenes convertidas:** {len(converted)}\n")
        f.write(f"- **Faltantes / sin archivo:** {len(missing)}\n")
        f.write(f"- **Errores de conversion:** {len(errors)}\n")
        f.write(f"- **Imagenes huerfanas** (en assets/ pero no en obras.json): {len(orphan_keys)}\n\n")
        f.write(f"| | |\n|---|---|\n")
        f.write(f"| Peso original total | {orig_mb:.1f} MB |\n")
        f.write(f"| Peso WebP total | {webp_mb:.1f} MB |\n")
        f.write(f"| Reduccion total | **{total_reduction}%** |\n\n")

        if missing:
            f.write("---\n\n## Imagenes faltantes o sin archivo\n\n")
            f.write("Estas obras aparecen en obras.json pero no tienen imagen en disco.\n\n")
            f.write("| ID | Titulo | Path en obras.json | Razon |\n")
            f.write("|----|--------|--------------------|-------|\n")
            for m in missing:
                f.write(f"| {m['id']} | {m['title']} | `{m['path']}` | {m['reason']} |\n")
            f.write("\n")

        if errors:
            f.write("---\n\n## Errores de conversion\n\n")
            for e in errors:
                f.write(f"- `[{e['id']}]` **{e['title']}** — `{e['path']}`  \n")
                f.write(f"  Error: {e['error']}\n")
            f.write("\n")

        if orphans_converted or orphans_errors:
            f.write("---\n\n## Imagenes huerfanas convertidas (no estan en obras.json)\n\n")
            f.write("| Original | WebP (KB) | Reduccion | Nueva ruta |\n")
            f.write("|----------|:---------:|:---------:|------------|\n")
            for o in orphans_converted:
                f.write(
                    f"| `{o['orig_path']}` "
                    f"| {o['webp_kb']} | {o['reduction']}% "
                    f"| `{o['webp_path']}` |\n"
                )
            for o in orphans_errors:
                f.write(f"| `{o['path']}` | — | ERROR: {o['error']} | — |\n")
            f.write("\n")

        f.write("---\n\n## Detalle de conversion\n\n")
        f.write("| ID | Titulo | Original (KB) | WebP (KB) | Reduccion | Nueva ruta |\n")
        f.write("|----|--------|:-------------:|:---------:|:---------:|------------|\n")
        for c in converted:
            f.write(
                f"| {c['id']} | {c['title']} "
                f"| {c['orig_kb']} | {c['webp_kb']} | {c['reduction']}% "
                f"| `{c['webp_path']}` |\n"
            )

    # ── Resumen final en consola ───────────────────────────────
    print(f"\nConvertidas : {len(converted)}")
    print(f"Faltantes   : {len(missing)}")
    print(f"Errores     : {len(errors)}")
    print(f"Huerfanas   : {len(orphan_keys)}  ({len(orphans_converted)} convertidas, {len(orphans_errors)} errores)")
    print(f"Original    : {orig_mb:.1f} MB")
    print(f"WebP        : {webp_mb:.1f} MB  ({total_reduction}% reduccion)")
    print(f"\nReporte     : info_conversion.md")
    print(f"WebP files  : assetswebp/")
    print("\nListo.")


if __name__ == "__main__":
    main()
