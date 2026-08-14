"""md-to-html: convierte un documento Markdown de resources/ a HTML autocontenido.

Uso:  python .github/tools/md-to-html.py <ruta.md> [ruta-salida.html]
      [--diagrams id1,id2,...] [--svg-dir <directorio>]

--diagrams reemplaza cada bloque mermaid del documento (en orden) por el SVG
correspondiente del directorio (ej. salida de drawio-to-svg.py), en vez de
renderizar el código con Mermaid JS.
Estilo: design system TriajeIA (cyan-salud).
Requiere: pip install markdown
"""

import re
import sys
from pathlib import Path

import markdown

CSS = """
:root{--primary:#0891B2;--accent:#059669;--bg:#FFFFFF;--fg:#164E63;--border:#A5F3FC;--code-bg:#ECFEFF;}
*{box-sizing:border-box}
body{margin:0;font-family:'Fira Sans','Segoe UI',system-ui,sans-serif;background:#F0F9FA;color:var(--fg);line-height:1.65;}
.wrap{max-width:960px;margin:0 auto;background:var(--bg);padding:48px 56px;box-shadow:0 0 24px rgba(8,145,178,.08);}
h1,h2,h3,h4{color:var(--primary);font-weight:600;line-height:1.3;}
h1{font-size:28px;border-bottom:3px solid var(--border);padding-bottom:12px;margin-bottom:8px;}
h2{font-size:22px;border-bottom:2px solid var(--border);padding-bottom:6px;margin-top:36px;}
h3{font-size:17px;margin-top:24px;}
h4{font-size:15px;color:#0E7490;}
p{margin:10px 0;}
code{background:var(--code-bg);color:#0E7490;padding:2px 6px;border-radius:4px;font-family:'Fira Code',Consolas,monospace;font-size:13px;}
pre{background:#164E63;color:#ECFEFF;padding:16px;border-radius:10px;overflow-x:auto;}
pre code{background:transparent;color:inherit;padding:0;font-size:13px;}
table{border-collapse:collapse;width:100%;margin:14px 0;font-size:14px;}
th{background:var(--primary);color:#fff;text-align:left;padding:8px 10px;}
td{border:1px solid var(--border);padding:8px 10px;vertical-align:top;}
tr:nth-child(even) td{background:#F7FDFE;}
blockquote{border-left:4px solid var(--primary);background:var(--code-bg);margin:12px 0;padding:8px 16px;color:#0E7490;font-size:14px;}
figure.diagram{margin:16px 0;text-align:center;border:1px solid var(--border);border-radius:10px;padding:12px;background:#FFF;}
figure.diagram svg{max-width:100%;height:auto;}
a{color:var(--accent);}
hr{border:none;border-top:2px solid var(--border);margin:28px 0;}
ul,ol{padding-left:24px;}
.footer{margin-top:40px;font-size:12px;color:#64748B;border-top:1px solid var(--border);padding-top:12px;}
@media print{body{background:#fff}.wrap{box-shadow:none;padding:0}}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">
{body}
<div class="footer">Generado con asistencia de IA · Kit-IA (skill archi) · {fecha} · Los diagramas están embebidos como imágenes SVG exportadas de
<code>Diagramas_TriajeIA.drawio</code> (11 pestañas).</div>
</div>
</body>
</html>
"""

MERMAID_RE = re.compile(r'<pre><code class="language-mermaid">.*?</code></pre>', re.DOTALL)


def replace_mermaid_with_svg(html: str, svg_ids: list, svg_dir: Path) -> str:
    """Reemplaza los bloques mermaid en orden por SVG inline."""
    blocks = MERMAID_RE.findall(html)
    if len(blocks) != len(svg_ids):
        print(
            f"AVISO: {len(blocks)} bloques mermaid vs {len(svg_ids)} diagramas indicados "
            "— se reemplazan los primeros coincidentes."
        )
    idx = 0

    def repl(_match):
        nonlocal idx
        if idx >= len(svg_ids):
            return _match.group(0)
        svg_file = svg_dir / f"{svg_ids[idx]}.svg"
        idx += 1
        if not svg_file.exists():
            print(f"AVISO: no existe {svg_file}")
            return _match.group(0)
        svg = svg_file.read_text(encoding="utf-8")
        return f'<figure class="diagram">{svg}</figure>'

    return MERMAID_RE.sub(repl, html)


def main() -> None:
    args = sys.argv[1:]
    diagrams: list = []
    svg_dir = None
    positional: list = []
    i = 0
    while i < len(args):
        if args[i] == "--diagrams" and i + 1 < len(args):
            diagrams = [d.strip() for d in args[i + 1].split(",") if d.strip()]
            i += 2
        elif args[i] == "--svg-dir" and i + 1 < len(args):
            svg_dir = Path(args[i + 1])
            i += 2
        else:
            positional.append(args[i])
            i += 1

    if not positional:
        print("Uso: python md-to-html.py <ruta.md> [salida.html] [--diagrams id1,id2] [--svg-dir dir]")
        sys.exit(2)
    src = Path(positional[0])
    out = Path(positional[1]) if len(positional) > 1 else src.with_suffix(".html")
    if diagrams:
        svg_dir = svg_dir or (src.parent / "diagramas-svg")
        if not svg_dir.exists():
            print(f"AVISO: directorio de SVG no existe: {svg_dir}")
    text = src.read_text(encoding="utf-8")
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "toc", "sane_lists"])
    if diagrams:
        body = replace_mermaid_with_svg(body, diagrams, svg_dir)
    title = text.splitlines()[0].lstrip("# ").strip() if text else src.stem
    html = TEMPLATE.format(title=title, css=CSS, body=body, fecha="2026-08-13")
    out.write_text(html, encoding="utf-8")
    print(f"OK: {out}")


if __name__ == "__main__":
    main()
