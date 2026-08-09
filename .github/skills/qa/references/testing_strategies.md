# Estrategias de Testing para Aplicaciones React y Next.js

Guía integral sobre arquitectura de tests, objetivos de cobertura y patrones de integración con CI/CD.

---

## Tabla de Contenidos

- [La Pirámide de Testing](#la-piramide-de-testing)
- [Análisis en Profundidad de los Tipos de Testing](#analisis-en-profundidad-de-los-tipos-de-testing)
- [Objetivos y Umbrales de Cobertura](#objetivos-y-umbrales-de-cobertura)
- [Patrones de Organización de Tests](#patrones-de-organizacion-de-tests)
- [Estrategias de Integración con CI/CD](#estrategias-de-integracion-con-cicd)
- [Marco de Decisión para Testing](#marco-de-decision-para-testing)

---

## La Pirámide de Testing

La pirámide de testing orienta cómo distribuir el esfuerzo de testing entre los distintos tipos de pruebas para obtener el ROI óptimo.

### Estructura Clásica de la Pirámide

```
        /\
       /  \      Pruebas E2E (5-10%)
      /----\     - Validación de recorridos de usuario
     /      \    - Cobertura de rutas críticas
    /--------\   Pruebas de Integración (20-30%)
   /          \  - Interacciones entre componentes
  /            \ - Integración de API
 /--------------\ Pruebas Unitarias (60-70%)
/                \ - Funciones individuales
------------------  - Componentes aislados
```

### Pirámide Adaptada a React/Next.js

Para aplicaciones frontend, la pirámide se ajusta levemente:

| Nivel | Porcentaje | Herramientas | Enfoque |
|-------|------------|-------|-------|
| Unitario | 50-60% | Jest o Vitest, RTL | Funciones puras, hooks, componentes aislados |
| Integración | 25-35% | RTL, MSW | Árboles de componentes, llamadas a API, contexto |
| E2E | 10-15% | Playwright | Flujos críticos de usuario, navegación entre páginas |

> **Jest o Vitest, no ambos.** Este skill no impone un runner unitario: usa el
> que el proyecto ya tenga instalado. Si arrancás de cero,
> `scripts/ensure-qa-dependencies.mjs --with-unit` detecta automáticamente
> cuál de los dos hay (o instala Jest por default si no hay ninguno) y nunca
> agrega el otro en paralelo. La API de asserts/mocks es prácticamente
> intercambiable entre ambos (`jest.fn()` ↔ `vi.fn()`, `jest.mock()` ↔
> `vi.mock()`, `jest.useFakeTimers()` ↔ `vi.useFakeTimers()`) — los ejemplos
> de este skill usan sintaxis de Jest; si tu proyecto usa Vitest, reemplazá
> `jest.*` por `vi.*` importado desde `'vitest'`.

### ¿Por Qué Esta Distribución?

**Las pruebas unitarias son rápidas y económicas:**
- Se ejecutan en milisegundos
- Permiten identificar fallas con precisión
- Son fáciles de mantener
- Se ejecutan en cada commit

**Las pruebas de integración equilibran cobertura y costo:**
- Prueban escenarios realistas
- Detectan errores de interacción entre componentes
- Tiempo de ejecución moderado
- Se ejecutan en cada PR

**Las pruebas E2E son costosas pero esenciales:**
- Validan la experiencia real del usuario
- Detectan problemas de despliegue
- Son lentas y frágiles (flaky)
- Se ejecutan en staging/producción

---

## Análisis en Profundidad de los Tipos de Testing

### Testing Unitario

**Propósito:** Verificar que unidades individuales de código funcionen correctamente de forma aislada.

**Qué Probar a Nivel Unitario:**
- Funciones utilitarias puras
- Hooks personalizados (con renderHook)
- Renderizado de componentes individuales
- Reducers de estado
- Lógica de validación
- Transformadores de datos

**Ejemplo: Testear una Función Pura**

```typescript
// utils/formatPrice.ts
export function formatPrice(cents: number, currency = 'USD'): string {
  const formatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  });
  return formatter.format(cents / 100);
}

// utils/formatPrice.test.ts
describe('formatPrice', () => {
  it('formats cents to USD by default', () => {
    expect(formatPrice(1999)).toBe('$19.99');
  });

  it('handles zero', () => {
    expect(formatPrice(0)).toBe('$0.00');
  });

  it('supports different currencies', () => {
    expect(formatPrice(1999, 'EUR')).toContain('€');
  });

  it('handles large numbers', () => {
    expect(formatPrice(100000000)).toBe('$1,000,000.00');
  });
});
```

**Ejemplo: Testear un Hook Personalizado**

```typescript
// hooks/useCounter.ts
export function useCounter(initial = 0) {
  const [count, setCount] = useState(initial);
  const increment = () => setCount(c => c + 1);
  const decrement = () => setCount(c => c - 1);
  const reset = () => setCount(initial);
  return { count, increment, decrement, reset };
}

// hooks/useCounter.test.ts
import { renderHook, act } from '@testing-library/react';
import { useCounter } from './useCounter';

describe('useCounter', () => {
  it('starts with initial value', () => {
    const { result } = renderHook(() => useCounter(5));
    expect(result.current.count).toBe(5);
  });

  it('increments count', () => {
    const { result } = renderHook(() => useCounter(0));
    act(() => result.current.increment());
    expect(result.current.count).toBe(1);
  });

  it('decrements count', () => {
    const { result } = renderHook(() => useCounter(5));
    act(() => result.current.decrement());
    expect(result.current.count).toBe(4);
  });

  it('resets to initial value', () => {
    const { result } = renderHook(() => useCounter(10));
    act(() => result.current.increment());
    act(() => result.current.reset());
    expect(result.current.count).toBe(10);
  });
});
```

### Testing de Integración

**Propósito:** Verificar que múltiples unidades funcionen correctamente en conjunto.

**Qué Probar a Nivel de Integración:**
- Árboles de componentes con múltiples hijos
- Componentes con proveedores de contexto
- Flujos de envío de formularios
- Manejo de llamadas a API y sus respuestas
- Interacciones de manejo de estado
- Componentes dependientes del router

**Ejemplo: Testear un Componente con Llamada a API**

```typescript
// components/UserProfile.tsx
export function UserProfile({ userId }: { userId: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(data => setUser(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  return <div>{user?.name}</div>;
}

// components/UserProfile.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { UserProfile } from './UserProfile';

const server = setupServer(
  rest.get('/api/users/:id', (req, res, ctx) => {
    return res(ctx.json({ id: req.params.id, name: 'John Doe' }));
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('UserProfile', () => {
  it('shows loading state initially', () => {
    render(<UserProfile userId="123" />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('displays user name after loading', async () => {
    render(<UserProfile userId="123" />);
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
  });

  it('displays error on API failure', async () => {
    server.use(
      rest.get('/api/users/:id', (req, res, ctx) => {
        return res(ctx.status(500));
      })
    );
    render(<UserProfile userId="123" />);
    await waitFor(() => {
      expect(screen.getByText(/Error/)).toBeInTheDocument();
    });
  });
});
```

### Testing End-to-End

**Propósito:** Verificar que los flujos completos de usuario funcionen en un entorno de navegador real.

**Qué Probar a Nivel E2E:**
- Flujos de negocio críticos (checkout, registro, login)
- Secuencias de navegación entre páginas
- Flujos de autenticación
- Integraciones con terceros
- Procesamiento de pagos
- Asistentes de formularios (wizards)

**Ejemplo: Testear el Flujo de Checkout**

```typescript
// e2e/checkout.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Checkout Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('completes purchase successfully', async ({ page }) => {
    // Agregar producto al carrito
    await page.goto('/products/widget-pro');
    await page.getByRole('button', { name: 'Add to Cart' }).click();

    // Verificar que el carrito se haya actualizado
    await expect(page.getByTestId('cart-count')).toHaveText('1');

    // Ir al checkout
    await page.getByRole('link', { name: 'Checkout' }).click();

    // Completar información de envío
    await page.getByLabel('Email').fill('test@example.com');
    await page.getByLabel('Address').fill('123 Test St');
    await page.getByLabel('City').fill('Test City');
    await page.getByLabel('Zip').fill('12345');

    // Completar información de pago (tarjeta de prueba)
    await page.getByLabel('Card Number').fill('4242424242424242');
    await page.getByLabel('Expiry').fill('12/25');
    await page.getByLabel('CVC').fill('123');

    // Enviar el pedido
    await page.getByRole('button', { name: 'Place Order' }).click();

    // Verificar la confirmación
    await expect(page).toHaveURL(/\/orders\/\w+/);
    await expect(page.getByText('Order Confirmed')).toBeVisible();
  });

  test('shows validation errors for invalid input', async ({ page }) => {
    await page.goto('/checkout');
    await page.getByRole('button', { name: 'Place Order' }).click();

    await expect(page.getByText('Email is required')).toBeVisible();
    await expect(page.getByText('Address is required')).toBeVisible();
  });
});
```

### Testing de Regresión Visual

**Propósito:** Detectar cambios visuales no intencionados en los componentes de la UI.

**Herramientas:** Comparaciones visuales de Playwright, Percy, Chromatic

**Ejemplo: Test de Snapshot Visual**

```typescript
// e2e/visual/components.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('button variants render correctly', async ({ page }) => {
    await page.goto('/storybook/button');
    await expect(page).toHaveScreenshot('button-variants.png');
  });

  test('responsive header', async ({ page }) => {
    // Escritorio
    await page.setViewportSize({ width: 1280, height: 720 });
    await page.goto('/');
    await expect(page.locator('header')).toHaveScreenshot('header-desktop.png');

    // Móvil
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('header')).toHaveScreenshot('header-mobile.png');
  });
});
```

### Testing de Accesibilidad

**Propósito:** Garantizar que la aplicación sea utilizable por personas con discapacidades.

**Herramientas:** jest-axe, @axe-core/playwright

**Ejemplo: Testing Automatizado de Accesibilidad**

```typescript
// Nivel Unitario/Integración con jest-axe
import { render } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import { Button } from './Button';

expect.extend(toHaveNoViolations);

describe('Button accessibility', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<Button>Click me</Button>);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});

// Nivel E2E con Playwright + Axe
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('homepage has no a11y violations', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

---

## Objetivos y Umbrales de Cobertura

### Umbrales Recomendados por Tipo de Proyecto

| Tipo de Proyecto | Statements | Branches | Functions | Lines |
|--------------|------------|----------|-----------|-------|
| Startup/MVP | 60% | 50% | 60% | 60% |
| Producto en Crecimiento | 75% | 70% | 75% | 75% |
| Empresarial | 85% | 80% | 85% | 85% |
| Crítico para la Seguridad | 95% | 90% | 95% | 95% |

### Cobertura por Tipo de Código

**Prioridad de Cobertura Alta (80%+):**
- Lógica de negocio
- Manejo de estado
- Manejadores de API
- Validación de formularios
- Autenticación/autorización
- Procesamiento de pagos

**Prioridad de Cobertura Media (60-80%):**
- Componentes de UI
- Funciones utilitarias
- Transformadores de datos
- Hooks personalizados

**Prioridad de Cobertura Baja (40-60%):**
- Páginas estáticas
- Wrappers simples
- Archivos de configuración
- Tipos/interfaces

### Configuración de Cobertura de Jest

```javascript
// jest.config.js
module.exports = {
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{ts,tsx}',
    '!src/**/index.{ts,tsx}', // archivos barrel
    '!src/types/**',
  ],
  coverageThreshold: {
    global: {
      statements: 80,
      branches: 75,
      functions: 80,
      lines: 80,
    },
    // Umbrales más altos para rutas críticas
    './src/services/payment/': {
      statements: 95,
      branches: 90,
      functions: 95,
      lines: 95,
    },
    './src/services/auth/': {
      statements: 90,
      branches: 85,
      functions: 90,
      lines: 90,
    },
  },
  coverageReporters: ['text', 'lcov', 'html', 'json'],
};
```

---

## Patrones de Organización de Tests

### Tests Co-ubicados (Recomendado para React)

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.test.tsx      # Pruebas unitarias
│   │   ├── Button.stories.tsx   # Storybook
│   │   └── index.ts
│   └── Form/
│       ├── Form.tsx
│       ├── Form.test.tsx
│       └── Form.integration.test.tsx  # Pruebas de integración
├── hooks/
│   ├── useAuth.ts
│   └── useAuth.test.ts
└── utils/
    ├── formatters.ts
    └── formatters.test.ts
```

### Directorio de Tests Separado

```
src/
├── components/
├── hooks/
└── utils/

__tests__/
├── unit/
│   ├── components/
│   ├── hooks/
│   └── utils/
├── integration/
│   └── flows/
└── fixtures/
    ├── users.json
    └── products.json

e2e/
├── specs/
│   ├── auth.spec.ts
│   └── checkout.spec.ts
├── fixtures/
│   └── auth.ts
└── pages/      # Modelos de Objetos de Página (Page Object Models)
    ├── LoginPage.ts
    └── CheckoutPage.ts
```

### Convenciones de Nombrado de Archivos de Test

| Patrón | Caso de Uso |
|---------|----------|
| `*.test.ts` | Pruebas unitarias |
| `*.spec.ts` | Pruebas de integración/E2E |
| `*.integration.test.ts` | Pruebas de integración explícitas |
| `*.e2e.spec.ts` | Pruebas E2E explícitas |
| `*.a11y.test.ts` | Pruebas de accesibilidad |
| `*.visual.spec.ts` | Pruebas de regresión visual |

---

## Estrategias de Integración con CI/CD

### Etapas del Pipeline

```yaml
# .github/workflows/test.yml
name: Test Pipeline

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  unit:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run test:unit -- --coverage
      - uses: codecov/codecov-action@v4
        with:
          files: coverage/lcov.info
          fail_ci_if_error: true

  integration:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: unit
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run test:integration

  e2e:
    name: E2E Tests
    runs-on: ubuntu-latest
    needs: integration
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npm run build
      - run: npx playwright test
      # Gate real: no basarse en el exit code de `playwright test` solo (eso
      # ya falla si un test individual falla), sino en el veredicto agregado
      # que calcula el propio skill QA a partir del manifest de evidencia
      # — considera severidad (`[critical]`) y bloqueados, no solo pass/fail.
      - run: node scripts/organize-evidence.mjs --results resources/qa/test-results/${{ github.run_id }}/results.json --out resources/qa
        if: always()
      - run: node scripts/generate-execution-report.mjs --manifest resources/qa/reports/${{ github.run_id }}-manifest.json --out resources/qa/reports/${{ github.run_id }}-execution-report.md --fail-on-no-go
        if: always()
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: qa-evidence-${{ github.run_id }}
          path: |
            resources/qa/*/${{ github.run_id }}
            resources/qa/reports/${{ github.run_id }}-manifest.json
            resources/qa/reports/${{ github.run_id }}-execution-report.md
          retention-days: 30
```

El paso de `generate-execution-report.mjs` corre con `if: always()` para que el
reporte y la evidencia se generen y suban aunque `playwright test` haya
fallado — pero `--fail-on-no-go` igual tumba el job si el veredicto agregado
es `NO-GO` (o usar `--fail-on-risk` si también se quiere bloquear en `GO with
known risks`). Ver `../SKILL.md` Paso 5 y `./video_evidence_guide.md`.

### División de Tests para Mayor Velocidad

```yaml
# Ejecutar pruebas E2E en paralelo en múltiples máquinas
e2e:
  strategy:
    matrix:
      shard: [1, 2, 3, 4]
  steps:
    - run: npx playwright test --shard=${{ matrix.shard }}/4
```

### Reglas de Bloqueo de PR (PR Gating)

| Tipo de Prueba | Cuándo Ejecutar | ¿Bloquea el Merge? |
|-----------|-------------|--------------|
| Unitaria | En cada commit | Sí |
| Integración | En cada PR | Sí |
| E2E (smoke) | En cada PR | Sí |
| E2E (completa) | Al hacer merge a main | No (solo alerta) |
| Visual | En cada PR | No (requiere revisión) |
| Rendimiento | Semanal/Release | No (solo alerta) |
| Veredicto QA agregado (`generate-execution-report.mjs --fail-on-no-go`) | En cada PR con E2E | Sí — bloquea en `NO-GO`, no solo en un test individual fallado |

---

## Marco de Decisión para Testing

### Cuándo Escribir Cada Tipo de Prueba

```
¿Es una función pura sin efectos secundarios?
├── Sí → Prueba unitaria
└── No
    ├── ¿Realiza llamadas a API o usa contexto?
    │   ├── Sí → Prueba de integración con mocking
    │   └── No
    │       ├── ¿Es un flujo crítico de usuario?
    │       │   ├── Sí → Prueba E2E
    │       │   └── No → Prueba de integración
    └── ¿Está enfocado en la UI con muchos estados visuales?
        ├── Sí → Storybook + Prueba visual
        └── No → Prueba unitaria de componente
```

### Matriz de ROI de Testing

| Tipo de Prueba | Tiempo de Escritura | Tiempo de Ejecución | Mantenimiento | Confianza |
|-----------|------------|----------|-------------|------------|
| Unitaria | Bajo | Muy rápido | Bajo | Media |
| Integración | Medio | Rápido | Medio | Alta |
| E2E | Alto | Lento | Alto | Muy alta |
| Visual | Bajo | Medio | Medio | Alta (UI) |

### Cuándo NO Testear

- Código generado (tipos de GraphQL, cliente de Prisma)
- Elementos internos de librerías de terceros
- Detalles de implementación (estado interno, métodos privados)
- Wrappers simples de paso directo (pass-through)
- Definiciones de tipos

### Señales de Alerta en la Estrategia de Testing

| Señal de Alerta | Problema | Solución |
|----------|---------|----------|
| Pruebas E2E > 30% | CI lento, tests flaky | Trasladar lógica hacia pruebas de integración |
| Solo pruebas unitarias | Faltan errores de interacción | Agregar pruebas de integración |
| Testear mocks | No se prueba el comportamiento real | Probar comportamiento, no implementación |
| Meta de cobertura del 100% | Rendimientos decrecientes | Enfocarse en las rutas críticas |
| Sin pruebas E2E | Faltan problemas de despliegue | Agregar smoke tests para flujos críticos |

---

## Resumen

1. **Seguir la pirámide:** 60% unitarias, 30% integración, 10% E2E
2. **Definir umbrales según el riesgo:** Mayor cobertura para las rutas críticas
3. **Co-ubicar los tests:** Mantener los tests cerca del código fuente
4. **Automatizar en CI:** Ejecutar tests en cada PR, bloquear merges ante fallas
5. **Decidir con criterio:** No todo necesita todos los tipos de test
