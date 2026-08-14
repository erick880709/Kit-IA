// Genera el Word del TFM TriajeIA a partir de los capítulos Markdown en
// resources/tfm/capitulos/ (kit-ia). Uso:
//   node .github/tools/generar-tfm-docx.js
// Salida: resources/tfm/TFM_TriajeIA_UNIR.docx
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, TableOfContents, BorderStyle, WidthType, PageBreak,
} = require("docx");

const RAIZ = path.resolve(__dirname, "..", "..");
const CAPITULOS = path.join(RAIZ, "resources", "tfm", "capitulos");
const SALIDA = path.join(RAIZ, "resources", "tfm", "TFM_TriajeIA_UNIR.docx");

function inline(texto) {
  // Negritas **x** y enlaces [[x|y]] → y
  const limpio = texto.replace(/\[\[([^\]]*\|)?([^\]]*)\]\]/g, "$2").trim();
  const partes = limpio.split(/(\*\*[^*]+\*\*)/g).filter(Boolean);
  return partes.map((p) =>
    p.startsWith("**") && p.endsWith("**")
      ? new TextRun({ text: p.slice(2, -2), bold: true })
      : new TextRun({ text: p })
  );
}

function parrafo(texto) {
  return new Paragraph({ children: inline(texto), spacing: { after: 120 } });
}

function lista(texto) {
  return new Paragraph({
    children: inline(texto.replace(/^-\s*/, "")),
    bullet: { level: 0 },
    spacing: { after: 80 },
  });
}

function tabla(filas) {
  const datos = filas.map((f) =>
    f.split("|").slice(1, -1).map((c) => c.trim())
  );
  const cabecera = datos[0];
  const cuerpo = datos.slice(2); // salta la línea de separación |---|
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: [
      new TableRow({
        children: cabecera.map(
          (c) =>
            new TableCell({
              children: [new Paragraph({ children: [new TextRun({ text: c, bold: true })] })],
              shading: { fill: "E8EEF7" },
            })
        ),
      }),
      ...cuerpo.map(
        (f) =>
          new TableRow({
            children: f.map(
              (c) =>
                new TableCell({
                  children: [new Paragraph({ children: inline(c) })],
                })
            ),
          })
      ),
    ],
  });
}

function capitulo(nombreArchivo) {
  const ruta = path.join(CAPITULOS, nombreArchivo);
  const texto = fs.readFileSync(ruta, "utf8");
  const lineas = texto.split(/\r?\n/);
  const hijos = [];
  let tablaPendiente = [];
  for (const linea of lineas) {
    if (linea.startsWith("|")) {
      tablaPendiente.push(linea);
      continue;
    }
    if (tablaPendiente.length) {
      hijos.push(tabla(tablaPendiente));
      tablaPendiente = [];
    }
    if (linea.startsWith("# ")) hijos.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: inline(linea.slice(2)) }));
    else if (linea.startsWith("## ")) hijos.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: inline(linea.slice(3)) }));
    else if (linea.startsWith("### ")) hijos.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: inline(linea.slice(4)) }));
    else if (linea.startsWith("- ")) hijos.push(lista(linea));
    else if (linea.startsWith("> ")) hijos.push(new Paragraph({ children: inline(linea.slice(2)).map((r) => { r.italics = true; return r; }) }));
    else if (linea.trim()) hijos.push(parrafo(linea));
  }
  if (tablaPendiente.length) hijos.push(tabla(tablaPendiente));
  return hijos;
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 140, after: 140 }, outlineLevel: 2 } },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 }, // A4 explícito
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      children: [
        // Portada
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 3600, after: 300 },
          children: [new TextRun({ text: "UNIVERSIDAD INTERNACIONAL DE LA RIOJA", bold: true, size: 28 })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 },
          children: [new TextRun({ text: "Máster Universitario en Inteligencia Artificial", size: 26 })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 900, after: 900 },
          children: [new TextRun({ text: "Desarrollo de un sistema de triaje multimodal basado en IA para la atención en urgencias médicas en Colombia", bold: true, size: 36 })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
          children: [new TextRun({ text: "Medina Betancur, Diego Andrés", size: 26 })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 },
          children: [new TextRun({ text: "Rivera Villanueva, Leyniker", size: 26 })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 600 },
          children: [new TextRun({ text: "Soto Díaz, Erick Duván", size: 26 })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 1200 },
          children: [new TextRun({ text: "Directora: Damaris Fuentes Lorenzo", size: 26 })] }),
        new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1200 },
          children: [new TextRun({ text: "Armenia, Colombia — 2026", size: 26 })] }),
        // Índice
        new Paragraph({ children: [new TableOfContents("Índice de contenidos")], pageBreakBefore: true }),
        ...capitulo("00-organizacion-trabajo-grupo.md"),
        ...capitulo("00-resumen-abstract.md"),
        ...capitulo("04-desarrollo-de-la-contribucion.md"),
        ...capitulo("05-resultados-experimentales.md"),
        ...capitulo("07-conclusiones-y-trabajo-futuro.md"),
      ],
    },
  ],
});

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(SALIDA, buffer);
  console.log("Generado:", SALIDA, `(${buffer.length} bytes)`);
});
