#!/usr/bin/env node
// Detecta y, si falta, instala automáticamente las herramientas de QA que
// este skill necesita para ejecutar pruebas — para que el usuario no tenga
// que instalar nada a mano antes de poder correr un plan de pruebas.
//
// Por defecto solo garantiza @playwright/test + sus navegadores (lo mínimo
// para E2E). Sumá flags según lo que el plan/runbook requiera:
//   --with-unit     Jest + React Testing Library (unitarias/integración)
//   --with-msw      Mock Service Worker (mocking de API)
//   --with-a11y     jest-axe + @axe-core/playwright (accesibilidad)
//   --skip-browsers No correr `playwright install` (ej. imagen de CI que ya los trae)
//   --dry-run       Mostrar qué se instalaría/ejecutaría sin instalar nada
//
// Uso:
//   node scripts/ensure-qa-dependencies.mjs [--with-unit] [--with-msw] [--with-a11y] [--skip-browsers] [--dry-run]
//
// Solo agrega devDependencies faltantes con el gestor de paquetes que ya
// usa el proyecto (detectado por lockfile); nunca instala nada global, ni
// actualiza/reemplaza una versión ya instalada.

import fs from 'node:fs';
import { execSync } from 'node:child_process';

const PACKAGE_GROUPS = {
  core: ['@playwright/test', 'dotenv'],
  unit: [
    'jest',
    '@testing-library/react',
    '@testing-library/jest-dom',
    '@testing-library/user-event',
  ],
  msw: ['msw'],
  a11y: ['jest-axe', '@axe-core/playwright'],
};

function parseArgs(argv) {
  return {
    withUnit: argv.includes('--with-unit'),
    withMsw: argv.includes('--with-msw'),
    withA11y: argv.includes('--with-a11y'),
    skipBrowsers: argv.includes('--skip-browsers'),
    dryRun: argv.includes('--dry-run'),
  };
}

function detectPackageManager() {
  if (fs.existsSync('bun.lockb')) return 'bun';
  if (fs.existsSync('pnpm-lock.yaml')) return 'pnpm';
  if (fs.existsSync('yarn.lock')) return 'yarn';
  return 'npm';
}

function installCommand(pm, packages) {
  const list = packages.join(' ');
  switch (pm) {
    case 'bun':
      return `bun add -d ${list}`;
    case 'pnpm':
      return `pnpm add -D ${list}`;
    case 'yarn':
      return `yarn add -D ${list}`;
    default:
      return `npm install -D ${list}`;
  }
}

function readPackageJson() {
  if (!fs.existsSync('package.json')) {
    console.error(
      'No se encontró package.json en el directorio actual. Corré este ' +
        'script desde la raíz del proyecto (donde vive package.json).'
    );
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync('package.json', 'utf8'));
}

function missingPackages(pkgJson, candidates) {
  const installed = {
    ...(pkgJson.dependencies || {}),
    ...(pkgJson.devDependencies || {}),
  };
  return candidates.filter((name) => !installed[name]);
}

function run(cmd, dryRun) {
  console.log(`$ ${cmd}`);
  if (dryRun) return;
  execSync(cmd, { stdio: 'inherit' });
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const pkgJson = readPackageJson();
  const pm = detectPackageManager();

  const wanted = [
    ...PACKAGE_GROUPS.core,
    ...(args.withUnit ? PACKAGE_GROUPS.unit : []),
    ...(args.withMsw ? PACKAGE_GROUPS.msw : []),
    ...(args.withA11y ? PACKAGE_GROUPS.a11y : []),
  ];

  const missing = missingPackages(pkgJson, wanted);

  if (missing.length === 0) {
    console.log('Todas las dependencias de QA solicitadas ya están instaladas.');
  } else {
    console.log(
      `Gestor de paquetes detectado: ${pm}. Instalando dependencias de QA faltantes como devDependency:`
    );
    console.log(`  ${missing.join(', ')}`);
    run(installCommand(pm, missing), args.dryRun);
  }

  if (!args.skipBrowsers && wanted.includes('@playwright/test')) {
    console.log('Asegurando navegadores de Playwright (chromium)...');
    // Idempotente: si ya están instalados, playwright install no vuelve a
    // descargar nada, así que es seguro correrlo siempre.
    run('npx playwright install --with-deps chromium', args.dryRun);
  }

  console.log(
    args.dryRun
      ? 'Dry-run: no se instaló ni ejecutó nada realmente.'
      : 'Listo: el proyecto tiene todo lo necesario para ejecutar las pruebas de este skill.'
  );
}

main();
