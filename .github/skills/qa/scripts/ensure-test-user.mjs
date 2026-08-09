#!/usr/bin/env node
// Garantiza que exista un usuario de prueba (email + password) antes de
// ejecutar pruebas que lo requieran. Si QA_USER_EMAIL/QA_USER_PASSWORD (o su
// equivalente --role admin) no están definidos en .env.qa, este script:
//   1. Genera un email y un password de prueba nuevos y seguros.
//   2. Si hay un endpoint de seed configurado (QA_SEED_API_URL), crea el
//      usuario ahí mismo vía API — es el camino preferido, no depende de UI.
//   3. Si no hay endpoint de seed, imprime instrucciones para que el agente
//      cree la cuenta a través del flujo real de registro/signup de la app
//      con Playwright, usando exactamente estas credenciales.
//   4. Persiste las credenciales (generadas o ya provistas) en .env.qa —
//      nunca en el runbook, el plan de pruebas, ni en ningún archivo versionado.
//
// Uso:
//   node scripts/ensure-test-user.mjs [--role user|admin] [--file .env.qa]
//
// No uses este patrón contra un entorno de producción real: está pensado
// para crear cuentas efímeras en un entorno de staging/QA dedicado a testing.

import fs from 'node:fs';
import crypto from 'node:crypto';

function parseArgs(argv) {
  const args = { role: 'user', envFile: '.env.qa' };
  for (let i = 0; i < argv.length; i += 1) {
    if (argv[i] === '--role') args.role = argv[++i];
    if (argv[i] === '--file') args.envFile = argv[++i];
  }
  if (!['user', 'admin'].includes(args.role)) {
    console.error('--role debe ser "user" o "admin"');
    process.exit(1);
  }
  return args;
}

function readEnvFile(envFile) {
  if (!fs.existsSync(envFile)) return {};
  const content = fs.readFileSync(envFile, 'utf8');
  const values = {};
  for (const line of content.split('\n')) {
    const match = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*?)\s*$/);
    if (match) values[match[1]] = match[2];
  }
  return values;
}

function upsertEnvFile(envFile, updates) {
  let content = fs.existsSync(envFile) ? fs.readFileSync(envFile, 'utf8') : '';
  for (const [key, value] of Object.entries(updates)) {
    const pattern = new RegExp(`^${key}=.*$`, 'm');
    const line = `${key}=${value}`;
    if (pattern.test(content)) {
      content = content.replace(pattern, line);
    } else {
      if (content.length > 0 && !content.endsWith('\n')) content += '\n';
      content += `${line}\n`;
    }
  }
  fs.writeFileSync(envFile, content);
}

function generatePassword() {
  // 20 caracteres, alfanuméricos + símbolos seguros, sin caracteres ambiguos.
  const charset =
    'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%^&*';
  const bytes = crypto.randomBytes(20);
  return Array.from(bytes, (b) => charset[b % charset.length]).join('');
}

function generateEmail(domain) {
  const slug = crypto.randomBytes(4).toString('hex');
  return `qa.${slug}@${domain}`;
}

async function seedViaApi(seedUrl, seedToken, email, password, role) {
  const res = await fetch(seedUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(seedToken ? { Authorization: `Bearer ${seedToken}` } : {}),
    },
    body: JSON.stringify({ email, password, role }),
  });
  if (!res.ok) {
    throw new Error(
      `El endpoint de seed respondió ${res.status} ${res.statusText}`
    );
  }
  return res;
}

async function main() {
  const { role, envFile } = parseArgs(process.argv.slice(2));
  const emailKey = role === 'admin' ? 'QA_ADMIN_EMAIL' : 'QA_USER_EMAIL';
  const passwordKey =
    role === 'admin' ? 'QA_ADMIN_PASSWORD' : 'QA_USER_PASSWORD';

  const env = { ...process.env, ...readEnvFile(envFile) };

  if (env[emailKey] && env[passwordKey]) {
    console.log(
      `${emailKey}/${passwordKey} ya están definidos en ${envFile}. Nada que hacer.`
    );
    return;
  }

  const domain = env.QA_TEST_EMAIL_DOMAIN || 'example.com';
  const email = env[emailKey] || generateEmail(domain);
  const password = env[passwordKey] || generatePassword();

  console.log(`No se encontró ${emailKey}/${passwordKey} en ${envFile}.`);
  console.log(`Generando credenciales de prueba nuevas para el rol "${role}":`);
  console.log(`  email:    ${email}`);
  console.log(`  password: ${password}`);

  if (env.QA_SEED_API_URL) {
    console.log(
      `Creando el usuario vía QA_SEED_API_URL (${env.QA_SEED_API_URL})...`
    );
    await seedViaApi(env.QA_SEED_API_URL, env.QA_SEED_API_TOKEN, email, password, role);
    console.log('Usuario creado vía API de seed.');
  } else {
    console.log(
      'No hay QA_SEED_API_URL configurado. Antes de ejecutar las pruebas, ' +
        'creá esta cuenta a través del flujo real de registro/signup de la ' +
        'aplicación usando exactamente este email y password. Si la app ' +
        'requiere verificación de email u otro paso manual, resolvelo ahora ' +
        'y confirmá que podés iniciar sesión con estas credenciales antes ' +
        'de continuar con la ejecución.'
    );
  }

  upsertEnvFile(envFile, { [emailKey]: email, [passwordKey]: password });
  console.log(
    `Credenciales guardadas en ${envFile}. No las repitas en el runbook, ` +
      'el plan de pruebas, ni en ningún archivo versionado.'
  );
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
