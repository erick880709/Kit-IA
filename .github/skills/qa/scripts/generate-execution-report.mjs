#!/usr/bin/env node
// Convierte resources/qa/reports/<runId>-manifest.json (producido por
// organize-evidence.mjs) en el reporte de ejecución en Markdown descrito en
// references/markdown_test_runbook.md, más un veredicto GO / GO-with-risks
// / NO-GO. Cada caso en el manifest apunta a su propia carpeta
// resources/qa/<CASE-ID>/<runId>/, que es donde vive la evidencia real.
//
// Uso (todos los entregables de este skill viven bajo resources/qa/ —
// ver SKILL.md#estructura-de-entregables-carpeta-de-salida; la carpeta de
// --out se crea automáticamente si no existe):
//   node scripts/generate-execution-report.mjs --manifest resources/qa/reports/<runId>-manifest.json --out resources/qa/reports/<runId>-execution-report.md

import fs from 'node:fs';
import path from 'node:path';

function parseArgs(argv) {
  const args = { manifest: null, out: null };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--manifest') args.manifest = argv[++i];
    if (argv[i] === '--out') args.out = argv[++i];
  }
  if (!args.manifest || !args.out) {
    console.error(
      'Uso: node generate-execution-report.mjs --manifest <manifest.json> --out <reporte.md>'
    );
    process.exit(1);
  }
  return args;
}

const STATUS_LABEL = {
  passed: 'passed',
  failed: 'failed',
  timedOut: 'failed',
  interrupted: 'blocked',
  skipped: 'not-run',
  unknown: 'not-run',
};

function computeVerdict(cases) {
  const failedCritical = cases.some(
    (c) => STATUS_LABEL[c.status] === 'failed' && c.priority === 'critical'
  );
  const anyFailedOrBlocked = cases.some((c) =>
    ['failed', 'blocked'].includes(STATUS_LABEL[c.status])
  );

  if (failedCritical) return 'NO-GO';
  if (anyFailedOrBlocked) return 'GO with known risks';
  return 'GO';
}

function main() {
  const { manifest: manifestPath, out } = parseArgs(process.argv.slice(2));
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  const cases = Object.values(manifest).sort((a, b) => {
    const pa = a.caseId || a.title;
    const pb = b.caseId || b.title;
    return pa.localeCompare(pb, undefined, { numeric: true });
  });

  const verdict = computeVerdict(cases);
  const total = cases.length;
  const counts = cases.reduce((acc, c) => {
    const label = STATUS_LABEL[c.status] || 'not-run';
    acc[label] = (acc[label] || 0) + 1;
    return acc;
  }, {});

  const rows = cases.map((c) => {
    const status = STATUS_LABEL[c.status] || 'not-run';
    const defect = c.error ? c.error.split('\n')[0].slice(0, 140) : '-';
    const evidence = Object.keys(c.artifacts).length
      ? Object.keys(c.artifacts).join(', ')
      : '-';
    const recording = c.artifacts['video.webm'] || c.artifacts['video.mp4'] || '-';
    return `| ${c.caseId || '-'} | ${c.title} | ${c.priority || '-'} | ${status} | ${defect} | ${evidence} | ${recording} |`;
  });

  const md = `# Reporte de Ejecución de QA

- Total de casos: ${total}
- Pasaron: ${counts.passed || 0}
- Fallaron: ${counts.failed || 0}
- Bloqueados: ${counts.blocked || 0}
- No ejecutados: ${counts['not-run'] || 0}
- **Veredicto: ${verdict}**

| Id de Caso | Título | Prioridad | Estado | Resumen del defecto | Evidencia | Grabación |
|---|---|---|---|---|---|---|
${rows.join('\n')}

## Notas

- "Grabación" apunta al archivo de video dentro de la carpeta \`resources/qa/<CASE-ID>/<runId>/\` correspondiente, producida por \`scripts/organize-evidence.mjs\`.
- Regla del veredicto: cualquier caso etiquetado \`[critical]\` que falle fuerza \`NO-GO\`; cualquier otro caso fallado/bloqueado fuerza \`GO with known risks\`; en cualquier otro caso, \`GO\`.
- Los casos sin un id \`TC-xxx\` reconocible en su título se listan con \`-\` y deberían corregirse en el origen (título de la prueba) para mantener la trazabilidad.
`;

  fs.mkdirSync(path.dirname(out), { recursive: true });
  fs.writeFileSync(out, md);
  console.log(`Reporte de ejecución escrito en ${out} (veredicto: ${verdict})`);
}

main();
