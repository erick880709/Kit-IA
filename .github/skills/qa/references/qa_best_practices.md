# Buenas Prácticas de QA para React y Next.js

Directrices para escribir tests mantenibles, depurar fallos y medir la calidad de los tests.

---

## Índice

- [Escribir Código Testeable](#escribir-codigo-testeable)
- [Convenciones de Nomenclatura de Tests](#convenciones-de-nomenclatura-de-tests)
- [Patrón Arrange-Act-Assert](#patron-arrange-act-assert)
- [Principios de Aislamiento de Tests](#principios-de-aislamiento-de-tests)
- [Gestión de Tests Inestables (Flaky)](#gestion-de-tests-inestables-flaky)
- [Revisión de Código para la Testeabilidad](#revision-de-codigo-para-la-testeabilidad)
- [Estrategias de Mantenimiento de Tests](#estrategias-de-mantenimiento-de-tests)
- [Depuración de Tests Fallidos](#depuracion-de-tests-fallidos)
- [Métricas de Calidad e Indicadores Clave (KPIs)](#metricas-de-calidad-e-indicadores-clave-kpis)

---

## Escribir Código Testeable

El código testeable es fácil de entender, tiene límites claros y minimiza las dependencias.

### Inyección de Dependencias

En lugar de crear dependencias dentro de las funciones, pásalas como parámetros.

**Difícil de testear:**

```typescript
// src/services/userService.ts
import { prisma } from '../lib/prisma';
import { sendEmail } from '../lib/email';

export async function createUser(data: UserInput) {
  const user = await prisma.user.create({ data });
  await sendEmail(user.email, 'Welcome!');
  return user;
}
```

**Fácil de testear:**

```typescript
// src/services/userService.ts
export function createUserService(
  db: PrismaClient,
  emailService: EmailService
) {
  return {
    async createUser(data: UserInput) {
      const user = await db.user.create({ data });
      await emailService.send(user.email, 'Welcome!');
      return user;
    },
  };
}

// Uso en la aplicación
const userService = createUserService(prisma, emailService);

// Uso en los tests
const mockDb = { user: { create: jest.fn() } };
const mockEmail = { send: jest.fn() };
const testService = createUserService(mockDb, mockEmail);
```

### Funciones Puras

Las funciones puras son deterministas y no tienen efectos secundarios, lo que las hace triviales de testear.

**Impura (difícil de testear):**

```typescript
function formatTimestamp() {
  const now = new Date();
  return `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}`;
}
```

**Pura (fácil de testear):**

```typescript
function formatTimestamp(date: Date): string {
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

// Test
expect(formatTimestamp(new Date('2024-03-15'))).toBe('2024-3-15');
```

### Separación de Responsabilidades

Separa la lógica de negocio de las operaciones de UI y de E/S.

**Responsabilidades mezcladas (difícil de testear):**

```typescript
// Componente con lógica de negocio embebida
function CheckoutForm() {
  const [total, setTotal] = useState(0);

  const handleSubmit = async (items: CartItem[]) => {
    // Lógica de negocio mezclada con la UI
    let sum = 0;
    for (const item of items) {
      sum += item.price * item.quantity;
      if (item.category === 'electronics') {
        sum *= 0.9; // 10% de descuento
      }
    }
    const tax = sum * 0.08;
    const finalTotal = sum + tax;

    // Llamada a la API
    await fetch('/api/orders', {
      method: 'POST',
      body: JSON.stringify({ items, total: finalTotal }),
    });

    setTotal(finalTotal);
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

**Responsabilidades separadas (fácil de testear):**

```typescript
// Lógica de negocio pura (fácil de testear unitariamente)
export function calculateOrderTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => {
    const subtotal = item.price * item.quantity;
    const discount = item.category === 'electronics' ? 0.9 : 1;
    return sum + subtotal * discount;
  }, 0);
}

export function calculateTax(subtotal: number, rate = 0.08): number {
  return subtotal * rate;
}

// Hook personalizado para la lógica del pedido (testeable con renderHook)
export function useCheckout() {
  const [total, setTotal] = useState(0);
  const mutation = useMutation(createOrder);

  const checkout = async (items: CartItem[]) => {
    const subtotal = calculateOrderTotal(items);
    const tax = calculateTax(subtotal);
    const finalTotal = subtotal + tax;

    await mutation.mutateAsync({ items, total: finalTotal });
    setTotal(finalTotal);
  };

  return { checkout, total, isLoading: mutation.isLoading };
}

// Componente (testeable mediante tests de integración)
function CheckoutForm() {
  const { checkout, total, isLoading } = useCheckout();
  return <form onSubmit={() => checkout(items)}>...</form>;
}
```

### Diseño de Componentes para la Testeabilidad

| Patrón | Testeabilidad | Ejemplo |
|---------|-------------|---------|
| Props en lugar de context | Alta | `<Button disabled={!valid}>` |
| Callbacks en lugar de efectos secundarios | Alta | `onSubmit={handleSubmit}` |
| Componentes controlados | Alta | `<Input value={value} onChange={...}>` |
| Render props | Media | `<DataProvider render={data => ...}>` |
| Estado interno | Baja | `const [x, setX] = useState()` |
| Estado global | Baja | `useGlobalStore()` |

---

## Convenciones de Nomenclatura de Tests

Los buenos nombres de tests documentan el comportamiento esperado y ayudan a diagnosticar fallos.

### Patrones de Nomenclatura

**Patrón 1: should [comportamiento esperado] when [condición]**

```typescript
describe('LoginForm', () => {
  it('should display error message when credentials are invalid', () => {});
  it('should redirect to dashboard when login succeeds', () => {});
  it('should disable submit button when form is submitting', () => {});
});
```

**Patrón 2: [método/acción] [resultado esperado]**

```typescript
describe('calculateDiscount', () => {
  it('returns 0 for orders under $50', () => {});
  it('returns 10% for orders $50-$99', () => {});
  it('returns 20% for orders $100+', () => {});
});
```

**Patrón 3: given [contexto], when [acción], then [resultado]**

```typescript
describe('ShoppingCart', () => {
  it('given an empty cart, when adding an item, then cart count is 1', () => {});
  it('given items in cart, when removing all, then cart is empty', () => {});
});
```

### Organización de Bloques Describe

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    describe('with valid input', () => {
      it('creates user in database', () => {});
      it('sends welcome email', () => {});
      it('returns user with id', () => {});
    });

    describe('with invalid input', () => {
      it('throws ValidationError for missing email', () => {});
      it('throws ValidationError for invalid email format', () => {});
      it('throws ConflictError for duplicate email', () => {});
    });
  });

  describe('deleteUser', () => {
    it('removes user from database', () => {});
    it('throws NotFoundError for non-existent user', () => {});
  });
});
```

### Antipatrones a Evitar

| Malo | Bueno | Por qué |
|-----|------|-----|
| `it('works')` | `it('returns sum of two numbers')` | Describe el comportamiento |
| `it('test 1')` | `it('handles empty array')` | Escenario específico |
| `it('should do stuff')` | `it('should validate email format')` | Expectativa clara |
| Duplicar código en el nombre | Describir el comportamiento | Salida legible |

---

## Patrón Arrange-Act-Assert

El patrón AAA estructura los tests en tres fases claras.

### Estructura

```typescript
it('calculates total with discount', () => {
  // Arrange - Preparar los datos y condiciones del test
  const items = [
    { name: 'Widget', price: 100, quantity: 2 },
    { name: 'Gadget', price: 50, quantity: 1 },
  ];
  const discountRate = 0.1;

  // Act - Ejecutar el código que se está testeando
  const result = calculateTotal(items, discountRate);

  // Assert - Verificar el resultado
  expect(result).toBe(225); // (200 + 50) * 0.9
});
```

### Ejemplo Asíncrono

```typescript
it('fetches user profile', async () => {
  // Arrange
  const userId = '123';
  server.use(
    rest.get('/api/users/:id', (req, res, ctx) =>
      res(ctx.json({ id: userId, name: 'John' }))
    )
  );

  // Act
  render(<UserProfile userId={userId} />);

  // Assert
  await expect(screen.findByText('John')).resolves.toBeInTheDocument();
});
```

### Ejemplo de Test de Componente

```typescript
it('submits form with user input', async () => {
  // Arrange
  const user = userEvent.setup();
  const onSubmit = jest.fn();
  render(<ContactForm onSubmit={onSubmit} />);

  // Act
  await user.type(screen.getByLabelText('Name'), 'John Doe');
  await user.type(screen.getByLabelText('Email'), 'john@example.com');
  await user.type(screen.getByLabelText('Message'), 'Hello!');
  await user.click(screen.getByRole('button', { name: 'Send' }));

  // Assert
  expect(onSubmit).toHaveBeenCalledWith({
    name: 'John Doe',
    email: 'john@example.com',
    message: 'Hello!',
  });
});
```

### Directrices

1. **Un Act por test** - Testear un comportamiento a la vez
2. **Múltiples aserciones están bien** - Si verifican el mismo comportamiento
3. **Evitar lógica en los tests** - Sin if/else ni bucles en el código de test
4. **Configuración en Arrange, no en beforeEach** - A menos que sea realmente compartida

---

## Principios de Aislamiento de Tests

Los tests aislados son independientes, repetibles y pueden ejecutarse en cualquier orden.

### Aislamiento de Estado

```typescript
describe('CartService', () => {
  let cartService: CartService;

  // Instancia nueva para cada test
  beforeEach(() => {
    cartService = new CartService();
  });

  it('adds item to empty cart', () => {
    cartService.addItem({ id: '1', quantity: 1 });
    expect(cartService.getItems()).toHaveLength(1);
  });

  it('starts with empty cart', () => {
    // No se ve afectado por el test anterior
    expect(cartService.getItems()).toHaveLength(0);
  });
});
```

### Aislamiento de Base de Datos

```typescript
describe('UserRepository', () => {
  beforeAll(async () => {
    // Conectar a la base de datos de test
    await db.connect(process.env.TEST_DATABASE_URL);
  });

  beforeEach(async () => {
    // Limpiar la base de datos antes de cada test
    await db.query('TRUNCATE users CASCADE');
  });

  afterAll(async () => {
    await db.disconnect();
  });

  it('creates user', async () => {
    const user = await userRepo.create({ email: 'test@example.com' });
    expect(user.id).toBeDefined();
  });
});
```

### Aislamiento de Mocking de API

```typescript
describe('ProductList', () => {
  // Restablecer los handlers después de cada test
  afterEach(() => server.resetHandlers());

  it('shows products from API', async () => {
    // El handler por defecto devuelve productos
    render(<ProductList />);
    await expect(screen.findByText('Widget')).resolves.toBeInTheDocument();
  });

  it('shows error on API failure', async () => {
    // Sobrescribir el handler solo para este test
    server.use(
      rest.get('/api/products', (req, res, ctx) =>
        res(ctx.status(500))
      )
    );

    render(<ProductList />);
    await expect(screen.findByText('Error')).resolves.toBeInTheDocument();
  });

  it('shows products again', async () => {
    // Vuelve al handler por defecto (se ejecutó server.resetHandlers)
    render(<ProductList />);
    await expect(screen.findByText('Widget')).resolves.toBeInTheDocument();
  });
});
```

### Checklist de Aislamiento

| Aspecto | Solución |
|--------|----------|
| Estado global | Restablecer en beforeEach |
| Temporizadores | jest.useFakeTimers() + jest.useRealTimers() |
| DOM | cleanup de RTL (automático) |
| Base de datos | Truncar tablas o usar transacciones |
| Mocks de API | server.resetHandlers() |
| Sistema de archivos | Usar directorios temporales, limpiar en afterEach |
| Variables de entorno | Restaurar en afterEach |

---

## Gestión de Tests Inestables (Flaky)

Los tests flaky pasan y fallan de forma intermitente sin cambios en el código.

### Causas Comunes y Soluciones

**1. Problemas de Sincronización (Timing)**

```typescript
// Flaky - condición de carrera
it('shows loading then data', () => {
  render(<UserProfile />);
  expect(screen.getByText('Loading')).toBeInTheDocument();
  expect(screen.getByText('John')).toBeInTheDocument(); // Puede fallar
});

// Corregido - manejo asíncrono adecuado
it('shows loading then data', async () => {
  render(<UserProfile />);
  expect(screen.getByText('Loading')).toBeInTheDocument();
  await waitFor(() => {
    expect(screen.getByText('John')).toBeInTheDocument();
  });
});
```

**2. Datos No Deterministas**

```typescript
// Flaky - datos aleatorios
it('sorts users alphabetically', () => {
  const users = [createUser(), createUser(), createUser()];
  // Los nombres son aleatorios, el orden es impredecible
});

// Corregido - datos deterministas
it('sorts users alphabetically', () => {
  const users = [
    createUser({ name: 'Charlie' }),
    createUser({ name: 'Alice' }),
    createUser({ name: 'Bob' }),
  ];
  const sorted = sortUsers(users);
  expect(sorted.map(u => u.name)).toEqual(['Alice', 'Bob', 'Charlie']);
});
```

**3. Dependencias de Orden entre Tests**

```typescript
// Flaky - depende del test anterior
describe('Counter', () => {
  const counter = new Counter(); // ¡Instancia compartida!

  it('increments', () => {
    counter.increment();
    expect(counter.value).toBe(1);
  });

  it('starts at zero', () => {
    expect(counter.value).toBe(0); // ¡Falla! El valor es 1
  });
});

// Corregido - instancia nueva por test
describe('Counter', () => {
  let counter: Counter;

  beforeEach(() => {
    counter = new Counter();
  });

  it('increments', () => {
    counter.increment();
    expect(counter.value).toBe(1);
  });

  it('starts at zero', () => {
    expect(counter.value).toBe(0); // Pasa
  });
});
```

**4. Dependencias de Red/Externas**

```typescript
// Flaky - llamada de red real
it('fetches data', async () => {
  const data = await fetch('https://api.example.com/data');
  expect(data).toBeDefined();
});

// Corregido - mockear la red
it('fetches data', async () => {
  server.use(
    rest.get('https://api.example.com/data', (req, res, ctx) =>
      res(ctx.json({ value: 42 }))
    )
  );

  const data = await fetchData();
  expect(data.value).toBe(42);
});
```

### Detección de Tests Flaky

```javascript
// jest.config.js
module.exports = {
  // Ejecutar cada test varias veces para detectar inestabilidad
  testEnvironment: 'jsdom',

  // Añadir reporters para hacer seguimiento de los tests flaky
  reporters: [
    'default',
    ['jest-junit', { outputDirectory: './reports' }],
  ],
};

// Ejecutar los tests varias veces
// npx jest --runInBand --testTimeout=10000 --repeat=5
```

### Estrategia de Cuarentena

1. **Identificar** - Hacer seguimiento de los tests que fallan aleatoriamente.
   Para E2E de Playwright organizados por este skill, no hace falta llevar
   esta cuenta a mano: `node ../scripts/flaky-trend.mjs --reports
   resources/qa/reports --out resources/qa/reports/flaky-trend.md` cruza los
   manifests de varias corridas (`resources/qa/reports/<runId>-manifest.json`)
   y calcula una tasa de flakiness real por caso (reintentos + cambios de
   estado entre ejecuciones), en vez de depender de percepción o memoria.
2. **Poner en cuarentena** - Moverlos a un conjunto separado, ejecutarlos aparte
3. **Corregir** - Investigar y solucionar la causa raíz
4. **Restaurar** - Devolverlos al conjunto principal

```typescript
// Omitir temporalmente un test flaky
it.skip('flaky test to fix', () => {
  // TODO: Corregir el problema de timing en #123
});

// O ejecutar solo cuando se está investigando
it.todo('investigate flaky behavior');
```

---

## Revisión de Código para la Testeabilidad

Preguntas que hacerse durante la revisión de código para garantizar código testeable.

### Checklist de Testeabilidad

**Funciones y Métodos:**
- [ ] ¿Tiene una única responsabilidad?
- [ ] ¿Las dependencias se inyectan?
- [ ] ¿Se puede testear sin mockear elementos internos?
- [ ] ¿Devuelve un valor o tiene efectos secundarios observables?

**Componentes:**
- [ ] ¿Las props son descriptivas y mínimas?
- [ ] ¿El comportamiento se puede activar mediante eventos de usuario?
- [ ] ¿Los estados de carga/error están expuestos?
- [ ] ¿Se puede renderizar sin un contexto completo de la aplicación?

**Gestión de Estado:**
- [ ] ¿El estado es mínimo y derivado siempre que sea posible?
- [ ] ¿Los cambios de estado se pueden activar y observar?
- [ ] ¿Los efectos secundarios están separados de los reducers?

### Comentarios de Revisión

**Antes:**
```typescript
// Difícil de testear - dependencia embebida
function processPayment(order: Order) {
  const stripe = new Stripe(process.env.STRIPE_KEY);
  return stripe.charges.create({
    amount: order.total,
    currency: 'usd',
  });
}
```

**Comentario de Revisión:**
> Considera inyectar el procesador de pagos para mejorar la testeabilidad:
> ```typescript
> function processPayment(order: Order, processor: PaymentProcessor) {
>   return processor.charge(order.total, 'usd');
> }
> ```
> Esto permite testear con un procesador mock sin llamar a la API de Stripe.

---

## Estrategias de Mantenimiento de Tests

Mantén los tests mantenibles a medida que evoluciona el código base.

### Reducir la Duplicación

**Usar helpers para aserciones comunes:**

```typescript
// __tests__/helpers/assertions.ts
export function expectLoadingState(container: HTMLElement) {
  expect(within(container).getByRole('progressbar')).toBeInTheDocument();
}

export function expectErrorState(container: HTMLElement, message: string) {
  expect(within(container).getByRole('alert')).toHaveTextContent(message);
}

// Uso
it('shows loading state', () => {
  render(<DataList />);
  expectLoadingState(screen.getByTestId('data-list'));
});
```

**Usar funciones factory:**

```typescript
// En lugar de repetir la configuración
function renderWithUser(ui: ReactElement, user = createUser()) {
  return {
    user,
    ...render(<AuthProvider user={user}>{ui}</AuthProvider>),
  };
}
```

### Actualizar los Tests Cuando Cambia el Código

**Escenario: Renombrar una prop**

```typescript
// Componente antiguo
<Button onClick={handleClick} />

// Componente nuevo
<Button onPress={handleClick} />

// Buscar y actualizar todos los tests
// grep -r "onClick" __tests__/ --include="*.test.tsx"
```

**Escenario: Cambiar la forma de la respuesta de la API**

```typescript
// Actualizar primero la factory
export function createUserResponse(overrides = {}) {
  return {
    user: {  // Nueva estructura anidada
      id: '1',
      name: 'Test User',
      ...overrides,
    },
  };
}

// Los tests obtienen automáticamente la nueva forma
```

### Cuándo Eliminar Tests

- **Cobertura redundante** - Varios tests que testean lo mismo
- **Testear la implementación** - Tests que se rompen al refactorizar
- **Funcionalidades obsoletas** - Tests de funcionalidad eliminada
- **Flaky sin remedio** - Tests que no se pueden estabilizar

### Documentación de Tests

```typescript
/**
 * @group integration
 * @requires database
 *
 * Tests para el flujo de procesamiento de pedidos.
 * Estos tests requieren una instancia de PostgreSQL en ejecución.
 *
 * Configuración: docker-compose up -d postgres
 */
describe('OrderProcessor', () => {
  /**
   * Verifica que los pedidos con artículos pendientes de reposición
   * se dividan en lotes de cumplimiento separados.
   *
   * Relacionado: JIRA-1234
   */
  it('splits orders with backordered items', () => {});
});
```

---

## Depuración de Tests Fallidos

Técnicas para investigar fallos en los tests.

### Depuración con Jest (o Vitest)

Los comandos de abajo usan Jest; si el proyecto usa Vitest, el equivalente
es `npx vitest run -t "..."` / `npx vitest <archivo>` / `npx vitest` (watch
es el modo por default de Vitest) — ver `../references/testing_strategies.md`
para la tabla de equivalencias Jest ↔ Vitest.

**Ejecutar un único test:**
```bash
# Por patrón de nombre
npx jest -t "should validate email"

# Por archivo
npx jest src/utils/__tests__/validation.test.ts

# Modo watch para iterar
npx jest --watch
```

**Depurar con el inspector de Node:**
```bash
node --inspect-brk node_modules/.bin/jest --runInBand
# Abrir chrome://inspect en Chrome
```

**Salida detallada (verbose):**
```bash
npx jest --verbose --no-coverage
```

### Depuración con React Testing Library

```typescript
it('renders user profile', async () => {
  render(<UserProfile userId="123" />);

  // Imprimir el DOM actual
  screen.debug();

  // Imprimir un elemento específico
  screen.debug(screen.getByRole('heading'));

  // Registrar los roles accesibles
  screen.logTestingPlaygroundURL(); // Abre el playground interactivo

  // Comprobar qué queries coincidirían
  const element = screen.getByRole('button');
  console.log(prettyDOM(element));
});
```

### Depuración con Playwright

```bash
# Modo debug - abre el navegador con el inspector
npx playwright test --debug

# Modo UI - ejecutor de tests visual
npx playwright test --ui

# Modo headed - ver el navegador
npx playwright test --headed

# Visor de trazas después de un fallo
npx playwright show-trace trace.zip
```

**Pausar dentro de un test:**
```typescript
test('debug this', async ({ page }) => {
  await page.goto('/');
  await page.pause(); // Abre el inspector
  await page.click('button');
});
```

### Patrones Comunes de Fallo

| Síntoma | Causa Probable | Enfoque de Depuración |
|---------|--------------|----------------|
| "Unable to find element" | Query incorrecta o elemento no renderizado | `screen.debug()`, comprobar lo asíncrono |
| "Expected X, received Y" | Error de lógica o mock desactualizado | Registrar valores intermedios |
| "Timeout exceeded" | Operación asíncrona lenta o falta de await | Aumentar el timeout, comprobar promesas |
| "Cannot read property of undefined" | Falta un mock o configuración | Comprobar beforeEach, valores devueltos por los mocks |
| Pasa en local, falla en CI | Diferencia de entorno | Comprobar variables de entorno, timing |

### Investigar Fallos Intermitentes (Flaky)

```typescript
// Añadir logging para fallos intermitentes
it('processes order', async () => {
  console.log('Test started at', Date.now());

  const order = await createOrder();
  console.log('Order created:', order.id);

  const result = await processOrder(order);
  console.log('Process result:', result);

  expect(result.status).toBe('completed');
});
```

---

## Métricas de Calidad e Indicadores Clave (KPIs)

Mide la efectividad de la suite de tests y haz seguimiento de las mejoras de calidad.

### Métricas Clave

**Métricas de Cobertura:**

| Métrica | Objetivo | Medición |
|--------|--------|-------------|
| Cobertura de líneas | 80% | `jest --coverage` |
| Cobertura de ramas | 75% | `jest --coverage` |
| Cobertura de funciones | 80% | `jest --coverage` |
| Cobertura de rutas críticas | 95% | Seguimiento personalizado |

**Salud de la Suite de Tests:**

| Métrica | Objetivo | Medición |
|--------|--------|-------------|
| Tasa de tests superados | 100% | Informes de CI |
| Tasa de tests flaky | <1% | Seguimiento de reintentos |
| Tiempo de ejecución de tests | <5 min | Tiempos de CI |
| Tests por componente | ≥3 | Cantidad de tests / componentes |

**Métricas de Defectos:**

| Métrica | Objetivo | Medición |
|--------|--------|-------------|
| Defectos encontrados en testing | >70% | Seguimiento de bugs |
| Defectos que llegan a producción | <10% | Bugs en producción |
| Tasa de regresión | <5% | Bugs reintroducidos |
| Tiempo medio de detección | <1 día | Marcas de tiempo de los bugs |

### Ejemplo de Dashboard

```typescript
// scripts/test-metrics.ts
import { readCoverageReport } from './utils';

const coverage = readCoverageReport('./coverage/coverage-summary.json');
const testResults = readTestReport('./reports/jest-results.json');

const metrics = {
  coverage: {
    lines: coverage.total.lines.pct,
    branches: coverage.total.branches.pct,
    functions: coverage.total.functions.pct,
  },
  tests: {
    total: testResults.numTotalTests,
    passed: testResults.numPassedTests,
    failed: testResults.numFailedTests,
    passRate: (testResults.numPassedTests / testResults.numTotalTests) * 100,
  },
  execution: {
    duration: testResults.testResults.reduce((sum, r) => sum + r.duration, 0),
  },
};

console.log('Test Metrics:', JSON.stringify(metrics, null, 2));
```

### Quality Gates de CI

```yaml
# .github/workflows/quality.yml
name: Quality Gates

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4

      - run: npm ci
      - run: npm test -- --coverage

      # Gate de cobertura
      - name: Check coverage
        run: |
          coverage=$(jq '.total.lines.pct' coverage/coverage-summary.json)
          if (( $(echo "$coverage < 80" | bc -l) )); then
            echo "Coverage $coverage% is below 80% threshold"
            exit 1
          fi

      # Gate de cantidad de tests
      - name: Check test count
        run: |
          tests=$(jq '.numTotalTests' reports/test-results.json)
          if [ "$tests" -lt 100 ]; then
            echo "Test count $tests is below minimum of 100"
            exit 1
          fi
```

### Seguimiento de Tendencias

Haz seguimiento de las métricas a lo largo del tiempo para identificar tendencias:

```typescript
// Recopilación semanal de métricas
{
  "week": "2024-W03",
  "coverage": {
    "lines": 82.4,
    "branches": 76.1,
    "trend": "+1.2%"  // vs. la semana anterior
  },
  "tests": {
    "total": 487,
    "new": 23,
    "removed": 5
  },
  "execution": {
    "avgDuration": 245,  // segundos
    "trend": "-12s"
  },
  "flaky": {
    "count": 3,
    "rate": 0.6
  }
}
```

---

## Resumen

1. **Escribe código testeable** - Inyecta dependencias, usa funciones puras, separa responsabilidades
2. **Nombra los tests con claridad** - Describe el comportamiento, no la implementación
3. **Sigue el patrón AAA** - Arrange, Act, Assert para una estructura clara
4. **Aísla los tests** - Estado nuevo, mocks restablecidos, sin dependencias entre tests
5. **Corrige los tests flaky** - Gestiona el timing, usa datos deterministas, mockea las dependencias externas
6. **Revisa la testeabilidad** - Compruébala durante la revisión de código, no después
7. **Mantén los tests** - Reduce la duplicación, actualízalos junto con los cambios de código
8. **Depura de forma sistemática** - Usa herramientas de depuración, registra información estratégicamente
9. **Mide la calidad** - Haz seguimiento de la cobertura, la tasa de éxito y el tiempo de ejecución
