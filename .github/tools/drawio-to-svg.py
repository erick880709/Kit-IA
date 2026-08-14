"""drawio-to-svg: exporta cada pestaña de un archivo .drawio a un archivo SVG.

Soporta las formas usadas en Diagramas_TriajeIA.drawio: rectángulos redondeados,
cilindros, actores UML, carpetas, texto, lifelines y aristas (con rutas ortogonales
simples y flechas). No requiere draw.io ni bibliotecas externas.

Uso:  python .github/tools/drawio-to-svg.py <archivo.drawio> <directorio-salida>
"""

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

NS = {"mx": "http://www.w3.org/1999/xhtml"}  # not used; cells are unnamespaced


def parse_style(style: str) -> dict:
    out: dict = {}
    for part in style.split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def escape(text: str) -> str:
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


def arrow_marker(color: str, marker_id: str) -> str:
    return (
        f'<marker id="{marker_id}" markerWidth="10" markerHeight="10" refX="8" '
        f'refY="3" orient="auto" markerUnits="strokeWidth">'
        f'<path d="M0,0 L0,6 L9,3 z" fill="{color}"/></marker>'
    )


def shape_svg(cell, geo, style, text_svg: str, text_x: float, text_y: float) -> str:
    x, y, w, h = geo
    fill = style.get("fillColor", "#FFFFFF") or "#FFFFFF"
    stroke = style.get("strokeColor", "#000000") or "#000000"
    dashed = 'stroke-dasharray="6 4"' if style.get("dashed") == "1" else ""
    kind = style.get("shape", "")

    if kind == "cylinder3":
        ry = min(14, h / 5)
        body = (
            f'<path d="M{x},{y + ry} L{x},{y + h - ry} '
            f'A{ry},{ry} 0 0 0 {x + w},{y + h - ry} L{x + w},{y + ry} '
            f'A{ry},{ry} 0 0 0 {x},{y + ry} Z" fill="{fill}" stroke="{stroke}" {dashed}/>'
            f'<ellipse cx="{x + w / 2}" cy="{y + ry}" rx="{w / 2}" ry="{ry}" '
            f'fill="{fill}" stroke="{stroke}" {dashed}/>'
        )
        return body + text_svg

    if kind == "umlActor":
        cx = x + w / 2
        head = f'<circle cx="{cx}" cy="{y + h * 0.18}" r="{min(w, h) * 0.09}" fill="{fill}" stroke="{stroke}"/>'
        body = (
            f'<path d="M{cx},{y + h * 0.33} L{cx},{y + h * 0.66} '
            f'M{cx - w * 0.32},{y + h * 0.46} L{cx + w * 0.32},{y + h * 0.46} '
            f'M{cx},{y + h * 0.66} L{cx - w * 0.3},{y + h * 0.92} '
            f'M{cx},{y + h * 0.66} L{cx + w * 0.3},{y + h * 0.92}" '
            f'fill="none" stroke="{stroke}" stroke-width="1.5" {dashed}/>'
        )
        label = text_svg
        return head + body + label

    if kind == "folder":
        tab = (
            f'<path d="M{x},{y + 12} L{x},{y + h} L{x + w},{y + h} L{x + w},{y + 12} '
            f'L{x + w * 0.55},{y + 12} L{x + w * 0.45},{y} L{x + 12},{y} Z" '
            f'fill="{fill}" stroke="{stroke}" {dashed}/>'
        )
        return tab + text_svg

    rx = 10 if style.get("rounded") == "1" else 0
    rect = (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" {dashed}/>'
    )
    return rect + text_svg


def text_block(value: str, x, y, w, h, style) -> str:
    lines = value.split("\n")
    size = int(style.get("fontSize", "12"))
    family = "Fira Code,Consolas,monospace" if "Courier" in style.get("fontFamily", "") else "Fira Sans,sans-serif"
    bold = ' font-weight="700"' if style.get("fontStyle") == "1" else ""
    italic = ' font-style="italic"' if style.get("fontStyle") == "2" else ""
    color = style.get("fontColor", "#164E63") or "#164E63"
    align = style.get("align", "center")
    n = len(lines)
    line_h = size + 4
    total = n * line_h
    top = y + (h - total) / 2 + size * 0.8
    out = []
    for i, line in enumerate(lines):
        ly = top + i * line_h
        if align == "left":
            out.append(
                f'<text x="{x + 8}" y="{ly}" font-family="{family}" font-size="{size}" '
                f'fill="{color}"{bold}{italic}>{escape(line)}</text>'
            )
        else:
            out.append(
                f'<text x="{x + w / 2}" y="{ly}" text-anchor="middle" '
                f'font-family="{family}" font-size="{size}" '
                f'fill="{color}"{bold}{italic}>{escape(line)}</text>'
            )
    return "".join(out)


def edge_route(src_geo, tgt_geo):
    """Ruta ortogonal simple de centro a centro, saliendo por el lado más directo."""
    sx, sy, sw, sh = src_geo
    tx, ty, tw, th = tgt_geo
    cxs, cys = sx + sw / 2, sy + sh / 2
    cxt, cyt = tx + tw / 2, ty + th / 2
    dx, dy = cxt - cxs, cyt - cys

    if abs(dx) >= abs(dy):
        if dx >= 0:
            ex = (sx + sw, cys)
            ix = (tx, cyt)
        else:
            ex = (sx, cys)
            ix = (tx + tw, cyt)
        return f"M{ex[0]},{ex[1]} L{ix[0]},{ex[1]} L{ix[0]},{ix[1]}", (ex[0], ex[1]), (ix[0], ix[1])
    if dy >= 0:
        ex = (cxs, sy + sh)
        ix = (cxt, ty)
    else:
        ex = (cxs, sy)
        ix = (cxt, ty + th)
    return f"M{ex[0]},{ex[1]} L{ex[0]},{ix[1]} L{ix[0]},{ix[1]}", ex, ix


def render_diagram(diagram) -> str:
    root = diagram.find("mxGraphModel/root")
    cells = list(root)
    vertices: dict = {}
    edges: list = []

    for cell in cells:
        if cell.tag != "mxCell":
            continue
        style = parse_style(cell.get("style", ""))
        geo_el = cell.find("mxGeometry")
        if cell.get("vertex") == "1":
            if geo_el is not None:
                x = float(geo_el.get("x", "0"))
                y = float(geo_el.get("y", "0"))
                w = float(geo_el.get("width", "120"))
                h = float(geo_el.get("height", "60"))
                vertices[cell.get("id")] = {
                    "value": cell.get("value", ""),
                    "style": style,
                    "geo": (x, y, w, h),
                }
        elif cell.get("edge") == "1":
            edges.append({"cell": cell, "style": style, "geo": geo_el})

    # Caja total
    xs = [v["geo"][0] for v in vertices.values()]
    ys = [v["geo"][1] for v in vertices.values()]
    x2 = [v["geo"][0] + v["geo"][2] for v in vertices.values()]
    y2 = [v["geo"][1] + v["geo"][3] for v in vertices.values()]
    min_x = min(xs + [0])
    min_y = min(ys + [0])
    max_x = max(x2 + [200])
    max_y = max(y2 + [200])
    pad = 30
    min_x -= pad
    min_y -= pad
    max_x += pad
    max_y += pad
    w_total = max_x - min_x
    h_total = max_y - min_y

    def off_x(v):
        return v - min_x

    def off_y(v):
        return v - min_y

    parts = []
    markers = []
    used_markers: set = set()

    def ensure_marker(color: str) -> str:
        mid = f"arr-{len(used_markers)}"
        used_markers.add(mid)
        markers.append(arrow_marker(color, mid))
        return mid

    # Aristas primero (debajo de los vértices)
    edge_labels = []
    for item in edges:
        cell, style, geo = item["cell"], item["style"], item["geo"]
        stroke = style.get("strokeColor", "#64748B") or "#64748B"
        dashed = 'stroke-dasharray="6 4"' if style.get("dashed") == "1" else ""
        mid = ensure_marker(stroke)
        src_id = cell.get("source")
        tgt_id = cell.get("target")
        if src_id and tgt_id and src_id in vertices and tgt_id in vertices:
            d, ex, ix = edge_route(vertices[src_id]["geo"], vertices[tgt_id]["geo"])
            path = f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="1.5" {dashed} marker-end="url(#{mid})"/>'
        elif geo is not None:
            sp = geo.find("mxPoint[@as='sourcePoint']")
            tp = geo.find("mxPoint[@as='targetPoint']")
            if sp is not None and tp is not None:
                x1 = off_x(float(sp.get("x")))
                y1 = off_y(float(sp.get("y")))
                x2 = off_x(float(tp.get("x")))
                y2 = off_y(float(tp.get("y")))
                path = (
                    f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{stroke}" '
                    f'stroke-width="1.5" {dashed} marker-end="url(#{mid})"/>'
                )
                ex, ix = (x1, y1), (x2, y2)
            else:
                continue
        else:
            continue
        parts.append(path)
        value = cell.get("value", "")
        if value:
            mx, my = (ex[0] + ix[0]) / 2, (ex[1] + ix[1]) / 2
            edge_labels.append(
                f'<g><rect x="{mx - 4}" y="{my - 11}" width="{len(value) * 6 + 8}" height="15" '
                f'fill="#FFFFFF" fill-opacity="0.85"/><text x="{mx}" y="{my}" text-anchor="middle" '
                f'font-size="11" font-family="Fira Sans,sans-serif" fill="{stroke}">{escape(value)}</text></g>'
            )

    # Vértices
    for vid, v in vertices.items():
        geo = v["geo"]
        gx, gy, gw, gh = off_x(geo[0]), off_y(geo[1]), geo[2], geo[3]
        style = v["style"]
        if style.get("verticalLine") == "1":
            parts.append(
                f'<line x1="{gx}" y1="{gy}" x2="{gx}" y2="{gy + gh}" '
                f'stroke="#64748B" stroke-dasharray="6 4"/>'
            )
            continue
        if not style and v["value"] == "":
            continue
        text_svg = text_block(v["value"], gx, gy, gw, gh, style) if v["value"] else ""
        if style.get("shape") == "umlActor" and v["value"]:
            label_y = gy + gh + 18
            text_svg = (
                f'<text x="{gx + gw / 2}" y="{label_y}" text-anchor="middle" '
                f'font-size="12" font-family="Fira Sans,sans-serif" fill="#164E63">'
                f'{escape(v["value"])}</text>'
            )
        parts.append(shape_svg(v["value"], (gx, gy, gw, gh), style, text_svg, 0, 0))

    parts.extend(edge_labels)
    defs = f"<defs>{''.join(markers)}</defs>" if markers else ""
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_total} {h_total}" '
        f'width="{w_total}" height="{h_total}" role="img" '
        f'aria-label="{escape(diagram.get("name", "diagrama"))}">'
        f"{defs}{''.join(parts)}</svg>"
    )
    return svg


def main() -> None:
    if len(sys.argv) < 3:
        print("Uso: python drawio-to-svg.py <archivo.drawio> <directorio-salida>")
        sys.exit(2)
    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    tree = ET.parse(src)
    mxfile = tree.getroot()
    count = 0
    for diagram in mxfile.findall("diagram"):
        did = diagram.get("id", f"d{count}")
        svg = render_diagram(diagram)
        out_file = out_dir / f"{did}.svg"
        out_file.write_text(svg, encoding="utf-8")
        print(f"OK: {out_file.name} ({diagram.get('name', did)})")
        count += 1
    print(f"Total: {count} SVG")


if __name__ == "__main__":
    main()
