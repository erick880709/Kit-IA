// Copiá este archivo a la raíz del proyecto como `playwright.config.ts` y
// ajustá `testDir`/`baseURL` según la estructura del proyecto. Carga los
// secretos desde `.env.qa` (ver references/env.example) — nunca los
// hardcodees acá.
import { defineConfig, devices } from '@playwright/test';
import * as dotenv from 'dotenv';

dotenv.config({ path: '.env.qa' });

// Cada ejecución obtiene su propia carpeta para que los videos/traces de
// distintas ejecuciones nunca se sobrescriban entre sí, y para que
// scripts/organize-evidence.mjs pueda agrupar los artefactos por ejecución.
const RUN_ID =
  process.env.QA_RUN_ID || new Date().toISOString().replace(/[:.]/g, '-');

// Todos los entregables de este skill viven bajo resources/qa/ en el
// proyecto — Playwright crea estas carpetas automáticamente si no existen.
const QA_ROOT = 'resources/qa';

// Sin pacing, Playwright ejecuta las acciones tan rápido como la app lo
// permite y el video grabado queda ilegible (clics a máxima velocidad, sin
// pausas visibles). slowMo agrega una demora fija entre acciones para que
// el video se pueda seguir a simple vista. Ver references/video_evidence_guide.md.
const SLOWMO_MS = Number(process.env.QA_SLOWMO_MS ?? 300);

export default defineConfig({
  testDir: './e2e',
  outputDir: `${QA_ROOT}/test-results/${RUN_ID}`,
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 2 : undefined,
  // Un test con muchos pasos y slowMo alto puede superar el timeout por
  // defecto de 30s; lo escalamos con un margen generoso por acción.
  timeout: 30_000 + SLOWMO_MS * 30,

  reporter: [
    ['list'],
    ['html', { outputFolder: `${QA_ROOT}/playwright-report/${RUN_ID}`, open: 'never' }],
    // El reporte JSON es lo que consume scripts/generate-execution-report.mjs.
    ['json', { outputFile: `${QA_ROOT}/test-results/${RUN_ID}/results.json` }],
  ],

  use: {
    baseURL: process.env.QA_BASE_URL,

    // Política de evidencia: capturar todo, en cada ejecución, para cada
    // caso. Cambiar a 'retain-on-failure' si el uso de disco se vuelve un
    // problema en el historial de CI de larga duración; también se puede
    // sobrescribir por spec con `test.use({ video: 'off' })` en specs de
    // baja prioridad.
    video: { mode: 'on', size: { width: 1280, height: 720 } },
    trace: 'on',
    screenshot: 'on',

    // Pausa entre acciones para que el video quede legible para una
    // persona (ver SLOWMO_MS arriba). Poné QA_SLOWMO_MS=0 para correr a
    // máxima velocidad en un gate de CI donde nadie va a mirar el video.
    launchOptions: {
      slowMo: SLOWMO_MS,
    },

    actionTimeout: 10_000,
    navigationTimeout: 15_000,
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    // Agregá más navegadores solo cuando el plan de pruebas lo requiera
    // explícitamente; cada proyecto extra multiplica el almacenamiento de
    // video/trace para los mismos escenarios.
  ],

  expect: {
    timeout: 5_000,
  },
});
