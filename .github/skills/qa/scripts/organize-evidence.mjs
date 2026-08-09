#!/usr/bin/env node
// Agrupa los adjuntos crudos de Playwright (video/trace/screenshot) por id
// de caso de prueba, creando una carpeta por caso directamente dentro de la
// raíz de entregables de QA (resources/qa/<CASE-ID>/<runId>/...), para que
// cada caso del runbook en Markdown mapee a su propia carpeta de evidencia.
//
// El runId se infiere del nombre de la carpeta que contiene results.json
// (la que generó playwright.config.template.ts, ej.
// resources/qa/test-results/<runId>/results.json), así no hay que pasarlo
// dos veces.
//
// Requiere que el reporter JSON de Playwright esté habilitado (ver
// scripts/playwright.config.template.ts) y que los títulos de las pruebas
// empiecen con un id de caso, ej.
// test('TC-01 - Login con credenciales válidas', ...).
//
// Uso (--out es la raíz de entregables de QA; se crea junto con cualquier
// subcarpeta que falte, ver SKILL.md#estructura-de-entregables-carpeta-de-salida):
//   node scripts/organize-evidence.mjs --results resources/qa/test-results/<runId>/results.json --out resources/qa
//
// Salida:
//   resources/qa/<CASE-ID>/<runId>/video.webm
//   resources/qa/<CASE-ID>/<runId>/trace.zip
//   resources/qa/<CASE-ID>/<runId>/screenshot-*.png
//   resources/qa/reports/<runId>-manifest.json   (id de caso -> estado, título, rutas de artefactos)

import fs from 'node:fs';
import path from 'node:path';

const CASE_ID_PATTERN = /\bTC-[A-Za-z0-9]+\b/i;

function parseArgs(argv) {
  const args = { results: null, out: null };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--results') args.results = argv[++i];
    if (argv[i] === '--out') args.out = argv[++i];
  }
  if (!args.results || !args.out) {
    console.error(
      'Uso: node organize-evidence.mjs --results <results.json> --out <resources/qa>'
    );
    process.exit(1);
  }
  return args;
}

function slugFallback(title) {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 60);
}

function collectTests(suite, acc = []) {
  for (const spec of suite.specs || []) {
    for (const test of spec.tests || []) {
      acc.push({ specTitle: spec.title, test });
    }
  }
  for (const child of suite.suites || []) {
    collectTests(child, acc);
  }
  return acc;
}

function main() {
  const { results, out } = parseArgs(process.argv.slice(2));

  // El runId es el nombre de la carpeta padre de results.json, ej.
  // resources/qa/test-results/2026-07-08T14-30-00Z/results.json -> "2026-07-08T14-30-00Z".
  const runId = path.basename(path.dirname(path.resolve(results)));

  const report = JSON.parse(fs.readFileSync(results, 'utf8'));
  const allTests = report.suites.flatMap((s) => collectTests(s));

  fs.mkdirSync(out, { recursive: true });
  const manifest = {};
  let missingCaseId = 0;

  for (const { specTitle, test } of allTests) {
    const match = specTitle.match(CASE_ID_PATTERN);
    const caseId = match ? match[0].toUpperCase() : null;
    if (!caseId) missingCaseId += 1;
    const folderName = caseId || slugFallback(specTitle);
    // Una carpeta por caso en la raíz de resources/qa/, con el runId
    // anidado adentro para conservar la evidencia de ejecuciones previas
    // del mismo caso en vez de sobrescribirla.
    const caseDir = path.join(out, folderName, runId);
    fs.mkdirSync(caseDir, { recursive: true });

    const lastResult = test.results[test.results.length - 1];
    const artifacts = {};
    let screenshotIndex = 0;

    for (const attachment of lastResult?.attachments || []) {
      if (!attachment.path) continue;
      const ext = path.extname(attachment.path) || '';
      let destName;
      if (attachment.name === 'video') destName = `video${ext}`;
      else if (attachment.name === 'trace') destName = `trace${ext}`;
      else if (attachment.contentType?.startsWith('image/')) {
        destName = `screenshot-${screenshotIndex++}${ext}`;
      } else {
        destName = path.basename(attachment.path);
      }
      const dest = path.join(caseDir, destName);
      fs.copyFileSync(attachment.path, dest);
      artifacts[destName] = dest;
    }

    const priorityMatch = specTitle.match(/\[(critical|high|medium|low)\]/i);

    manifest[caseId || folderName] = {
      caseId: caseId || null,
      title: specTitle,
      priority: priorityMatch ? priorityMatch[1].toLowerCase() : null,
      status: lastResult?.status || 'unknown',
      retries: test.results.length - 1,
      durationMs: lastResult?.duration ?? null,
      error: lastResult?.error?.message || null,
      caseDir,
      artifacts,
    };
  }

  const reportsDir = path.join(out, 'reports');
  fs.mkdirSync(reportsDir, { recursive: true });
  const manifestPath = path.join(reportsDir, `${runId}-manifest.json`);
  fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));

  console.log(
    `Evidencia organizada para ${allTests.length} prueba(s) — una carpeta por caso en ${out}/<CASE-ID>/${runId}/`
  );
  console.log(`Manifest escrito en ${manifestPath}`);
  if (missingCaseId > 0) {
    console.warn(
      `${missingCaseId} prueba(s) no tenían un id de caso "TC-xxx" en su título; ` +
        'se agruparon por título slugificado en su lugar. Agregá ids de ' +
        'caso a los títulos para tener trazabilidad limpia contra el runbook en Markdown.'
    );
  }
}

main();
