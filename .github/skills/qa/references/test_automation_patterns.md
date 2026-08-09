# Patrones de Automatización de Pruebas para React y Next.js

Patrones reutilizables para estructurar código de pruebas, simular (mock) dependencias y manejar operaciones asíncronas.

---

## Tabla de Contenidos

- [Page Object Model para React](#page-object-model-para-react)
- [Factories de Datos de Prueba](#factories-de-datos-de-prueba)
- [Gestión de Fixtures](#gestion-de-fixtures)
- [Estrategias de Mocking](#estrategias-de-mocking)
- [Utilidades de Prueba Personalizadas](#utilidades-de-prueba-personalizadas)
- [Patrones de Pruebas Asíncronas](#patrones-de-pruebas-asincronas)
- [Guía de Snapshot Testing](#guia-de-snapshot-testing)

---

## Page Object Model para React

El Page Object Model (POM) encapsula las interacciones de página en clases reutilizables, reduciendo el mantenimiento de las pruebas.

### Page Objects de Playwright

```typescript
// e2e/pages/LoginPage.ts
import { Page, Locator, expect } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel('Email');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
    this.errorMessage = page.getByRole('alert');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }

  async expectError(message: string) {
    await expect(this.errorMessage).toContainText(message);
  }

  async expectRedirectToDashboard() {
    await expect(this.page).toHaveURL('/dashboard');
  }
}
```

**Uso en las pruebas:**

```typescript
// e2e/auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from './pages/LoginPage';

test.describe('Authentication', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.goto();
  });

  test('successful login redirects to dashboard', async () => {
    await loginPage.login('user@example.com', 'password123');
    await loginPage.expectRedirectToDashboard();
  });

  test('invalid credentials show error', async () => {
    await loginPage.login('user@example.com', 'wrongpassword');
    await loginPage.expectError('Invalid credentials');
  });
});
```

### Component Object Model (React Testing Library)

```typescript
// __tests__/objects/LoginFormObject.ts
import { screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

export class LoginFormObject {
  get emailInput() {
    return screen.getByLabelText(/email/i);
  }

  get passwordInput() {
    return screen.getByLabelText(/password/i);
  }

  get submitButton() {
    return screen.getByRole('button', { name: /sign in/i });
  }

  get errorMessage() {
    return screen.queryByRole('alert');
  }

  async fillEmail(email: string) {
    await userEvent.type(this.emailInput, email);
  }

  async fillPassword(password: string) {
    await userEvent.type(this.passwordInput, password);
  }

  async submit() {
    await userEvent.click(this.submitButton);
  }

  async login(email: string, password: string) {
    await this.fillEmail(email);
    await this.fillPassword(password);
    await this.submit();
  }

  async expectError(message: string) {
    await waitFor(() => {
      expect(this.errorMessage).toHaveTextContent(message);
    });
  }
}
```

### Cuándo usar POM

| Escenario | ¿Usar POM? |
|----------|----------|
| Páginas complejas con muchas interacciones | Sí |
| Componentes reutilizables probados en varias suites | Sí |
| Pruebas simples de un solo uso | No (excesivo) |
| Pruebas E2E con flujos compartidos | Sí |

---

## Factories de Datos de Prueba

Las factories crean datos de prueba con valores por defecto razonables, reduciendo el código repetitivo y mejorando la mantenibilidad.

### Patrón de Factory Básico

```typescript
// __tests__/factories/userFactory.ts
interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user' | 'guest';
  createdAt: Date;
  preferences: {
    theme: 'light' | 'dark';
    notifications: boolean;
  };
}

let idCounter = 0;

export function createUser(overrides: Partial<User> = {}): User {
  return {
    id: `user-${++idCounter}`,
    email: `user${idCounter}@example.com`,
    name: `Test User ${idCounter}`,
    role: 'user',
    createdAt: new Date('2024-01-01'),
    preferences: {
      theme: 'light',
      notifications: true,
    },
    ...overrides,
    // Combinar en profundidad (deep merge) las preferencias si se proporcionan
    preferences: {
      theme: 'light',
      notifications: true,
      ...overrides.preferences,
    },
  };
}

// Builders especializados
export function createAdmin(overrides: Partial<User> = {}): User {
  return createUser({ role: 'admin', ...overrides });
}

export function createGuest(overrides: Partial<User> = {}): User {
  return createUser({
    role: 'guest',
    name: 'Guest',
    email: '',
    ...overrides,
  });
}
```

### Builder Pattern para objetos complejos

```typescript
// __tests__/factories/orderBuilder.ts
interface OrderItem {
  productId: string;
  quantity: number;
  price: number;
}

interface Order {
  id: string;
  userId: string;
  items: OrderItem[];
  status: 'pending' | 'processing' | 'shipped' | 'delivered';
  total: number;
  shippingAddress: Address;
  createdAt: Date;
}

export class OrderBuilder {
  private order: Partial<Order> = {};
  private items: OrderItem[] = [];

  withId(id: string): this {
    this.order.id = id;
    return this;
  }

  forUser(userId: string): this {
    this.order.userId = userId;
    return this;
  }

  withItem(productId: string, quantity: number, price: number): this {
    this.items.push({ productId, quantity, price });
    return this;
  }

  withStatus(status: Order['status']): this {
    this.order.status = status;
    return this;
  }

  shippedTo(address: Address): this {
    this.order.shippingAddress = address;
    return this;
  }

  build(): Order {
    const total = this.items.reduce(
      (sum, item) => sum + item.price * item.quantity,
      0
    );

    return {
      id: this.order.id || `order-${Date.now()}`,
      userId: this.order.userId || 'user-1',
      items: this.items,
      status: this.order.status || 'pending',
      total,
      shippingAddress: this.order.shippingAddress || createAddress(),
      createdAt: new Date(),
    };
  }
}

// Uso
const order = new OrderBuilder()
  .forUser('user-123')
  .withItem('product-1', 2, 29.99)
  .withItem('product-2', 1, 49.99)
  .withStatus('processing')
  .build();
```

### Factory con Faker

```typescript
// __tests__/factories/productFactory.ts
import { faker } from '@faker-js/faker';

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
  inStock: boolean;
  imageUrl: string;
}

export function createProduct(overrides: Partial<Product> = {}): Product {
  return {
    id: faker.string.uuid(),
    name: faker.commerce.productName(),
    description: faker.commerce.productDescription(),
    price: parseFloat(faker.commerce.price({ min: 10, max: 500 })),
    category: faker.commerce.department(),
    inStock: faker.datatype.boolean({ probability: 0.8 }),
    imageUrl: faker.image.url(),
    ...overrides,
  };
}

export function createProducts(count: number): Product[] {
  return Array.from({ length: count }, () => createProduct());
}
```

---

## Gestión de Fixtures

Los fixtures proporcionan datos de prueba y configuración consistentes en las distintas suites de pruebas.

### Fixtures de Playwright

```typescript
// e2e/fixtures/auth.ts
import { test as base, Page } from '@playwright/test';
import { createUser } from '../factories/userFactory';

interface AuthFixtures {
  authenticatedPage: Page;
  adminPage: Page;
  testUser: ReturnType<typeof createUser>;
}

export const test = base.extend<AuthFixtures>({
  testUser: async ({}, use) => {
    const user = createUser();
    await use(user);
  },

  authenticatedPage: async ({ page, testUser }, use) => {
    // Iniciar sesión vía API para omitir la UI
    await page.request.post('/api/auth/login', {
      data: {
        email: testUser.email,
        password: 'testpassword',
      },
    });

    // Obtener la cookie de sesión
    const cookies = await page.context().cookies();
    await page.context().addCookies(cookies);

    await use(page);
  },

  adminPage: async ({ page }, use) => {
    const admin = createUser({ role: 'admin' });

    await page.request.post('/api/auth/login', {
      data: {
        email: admin.email,
        password: 'adminpassword',
      },
    });

    await use(page);
  },
});

export { expect } from '@playwright/test';
```

**Uso de fixtures personalizados:**

```typescript
// e2e/dashboard.spec.ts
import { test, expect } from './fixtures/auth';

test('dashboard shows user name', async ({ authenticatedPage, testUser }) => {
  await authenticatedPage.goto('/dashboard');
  await expect(authenticatedPage.getByText(testUser.name)).toBeVisible();
});

test('admin sees admin panel', async ({ adminPage }) => {
  await adminPage.goto('/dashboard');
  await expect(adminPage.getByText('Admin Panel')).toBeVisible();
});
```

### Configuración de pruebas de Jest

```typescript
// jest.setup.ts
import '@testing-library/jest-dom';
import { server } from './__tests__/mocks/server';

// Iniciar el servidor de MSW antes de todas las pruebas
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));

// Restablecer los handlers después de cada prueba
afterEach(() => server.resetHandlers());

// Limpiar después de todas las pruebas
afterAll(() => server.close());

// Mock de window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock de IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  observe() {}
  unobserve() {}
  disconnect() {}
};
```

### Archivos de datos de prueba compartidos

```typescript
// __tests__/fixtures/products.json
{
  "products": [
    {
      "id": "prod-1",
      "name": "Widget Pro",
      "price": 29.99,
      "category": "Electronics"
    },
    {
      "id": "prod-2",
      "name": "Gadget Plus",
      "price": 49.99,
      "category": "Electronics"
    }
  ]
}

// __tests__/fixtures/index.ts
import productsData from './products.json';
import usersData from './users.json';

export const fixtures = {
  products: productsData.products,
  users: usersData.users,
};
```

---

## Estrategias de Mocking

### MSW (Mock Service Worker) para mocking de API

MSW intercepta las solicitudes de red a nivel de service worker, funcionando tanto en el navegador como en Node.

**Configuración de handlers:**

```typescript
// __tests__/mocks/handlers.ts
import { rest } from 'msw';
import { createUser } from '../factories/userFactory';
import { createProduct } from '../factories/productFactory';

export const handlers = [
  // GET /api/users/:id
  rest.get('/api/users/:id', (req, res, ctx) => {
    const { id } = req.params;
    const user = createUser({ id: id as string });
    return res(ctx.json(user));
  }),

  // GET /api/products
  rest.get('/api/products', (req, res, ctx) => {
    const category = req.url.searchParams.get('category');
    const products = Array.from({ length: 10 }, () => createProduct());
    const filtered = category
      ? products.filter(p => p.category === category)
      : products;
    return res(ctx.json(filtered));
  }),

  // POST /api/orders
  rest.post('/api/orders', async (req, res, ctx) => {
    const body = await req.json();
    return res(
      ctx.status(201),
      ctx.json({
        id: `order-${Date.now()}`,
        ...body,
        status: 'pending',
      })
    );
  }),

  // Simulación de error
  rest.get('/api/error', (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({ error: 'Internal Server Error' })
    );
  }),
];
```

**Configuración del servidor:**

```typescript
// __tests__/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

**Sobrescribiendo handlers en las pruebas:**

```typescript
// __tests__/components/ProductList.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { server } from '../mocks/server';
import { ProductList } from '../../src/components/ProductList';

describe('ProductList', () => {
  it('shows loading state', () => {
    render(<ProductList />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('renders products', async () => {
    render(<ProductList />);
    await waitFor(() => {
      expect(screen.getAllByTestId('product-card')).toHaveLength(10);
    });
  });

  it('shows error state on API failure', async () => {
    server.use(
      rest.get('/api/products', (req, res, ctx) => {
        return res(ctx.status(500));
      })
    );

    render(<ProductList />);
    await waitFor(() => {
      expect(screen.getByText(/error loading products/i)).toBeInTheDocument();
    });
  });

  it('shows empty state when no products', async () => {
    server.use(
      rest.get('/api/products', (req, res, ctx) => {
        return res(ctx.json([]));
      })
    );

    render(<ProductList />);
    await waitFor(() => {
      expect(screen.getByText('No products found')).toBeInTheDocument();
    });
  });
});
```

### Mocking de módulos con Jest

```typescript
// Mockear un módulo
jest.mock('../../src/services/analytics', () => ({
  trackEvent: jest.fn(),
  trackPageView: jest.fn(),
  setUser: jest.fn(),
}));

// Mockear con implementación
jest.mock('next/router', () => ({
  useRouter: jest.fn().mockReturnValue({
    pathname: '/test',
    push: jest.fn(),
    replace: jest.fn(),
    query: {},
  }),
}));

// Mock parcial (conserva algunas implementaciones reales)
jest.mock('../../src/utils/helpers', () => ({
  ...jest.requireActual('../../src/utils/helpers'),
  sendEmail: jest.fn().mockResolvedValue({ success: true }),
}));
```

### Mocking de hooks

```typescript
// __tests__/hooks/useAuth.test.tsx
import { renderHook, act } from '@testing-library/react';
import { useAuth } from '../../src/hooks/useAuth';
import * as authService from '../../src/services/auth';

jest.mock('../../src/services/auth');

const mockAuthService = authService as jest.Mocked<typeof authService>;

describe('useAuth', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('logs in user successfully', async () => {
    const mockUser = { id: '1', email: 'test@example.com' };
    mockAuthService.login.mockResolvedValue(mockUser);

    const { result } = renderHook(() => useAuth());

    await act(async () => {
      await result.current.login('test@example.com', 'password');
    });

    expect(result.current.user).toEqual(mockUser);
    expect(result.current.isAuthenticated).toBe(true);
  });

  it('handles login error', async () => {
    mockAuthService.login.mockRejectedValue(new Error('Invalid credentials'));

    const { result } = renderHook(() => useAuth());

    await act(async () => {
      try {
        await result.current.login('test@example.com', 'wrong');
      } catch (e) {
        // Esperado
      }
    });

    expect(result.current.user).toBeNull();
    expect(result.current.error).toBe('Invalid credentials');
  });
});
```

---

## Utilidades de Prueba Personalizadas

### Render con Providers

```typescript
// __tests__/utils/renderWithProviders.tsx
import React, { ReactElement } from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from '../../src/contexts/ThemeContext';
import { AuthProvider } from '../../src/contexts/AuthContext';

interface ExtendedRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  initialUser?: User | null;
  theme?: 'light' | 'dark';
}

export function renderWithProviders(
  ui: ReactElement,
  {
    initialUser = null,
    theme = 'light',
    ...renderOptions
  }: ExtendedRenderOptions = {}
) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false, // Deshabilitar reintentos en las pruebas
      },
    },
  });

  function Wrapper({ children }: { children: React.ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        <AuthProvider initialUser={initialUser}>
          <ThemeProvider initialTheme={theme}>
            {children}
          </ThemeProvider>
        </AuthProvider>
      </QueryClientProvider>
    );
  }

  return {
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
    queryClient,
  };
}

// Reexportar todo desde RTL
export * from '@testing-library/react';
export { renderWithProviders as render };
```

**Uso:**

```typescript
// __tests__/components/Dashboard.test.tsx
import { render, screen } from '../utils/renderWithProviders';
import { Dashboard } from '../../src/components/Dashboard';
import { createUser } from '../factories/userFactory';

describe('Dashboard', () => {
  it('shows user greeting when authenticated', () => {
    const user = createUser({ name: 'John Doe' });
    render(<Dashboard />, { initialUser: user });
    expect(screen.getByText('Hello, John Doe')).toBeInTheDocument();
  });

  it('shows login prompt when not authenticated', () => {
    render(<Dashboard />, { initialUser: null });
    expect(screen.getByText('Please log in')).toBeInTheDocument();
  });

  it('applies dark theme', () => {
    render(<Dashboard />, { theme: 'dark' });
    expect(document.body).toHaveClass('dark');
  });
});
```

### Matchers personalizados

```typescript
// __tests__/utils/customMatchers.ts
import { expect } from '@playwright/test';

expect.extend({
  async toHaveLoadedSuccessfully(page) {
    const hasNoErrors = await page.evaluate(() => {
      return !document.querySelector('[data-error]');
    });
    const isLoaded = await page.evaluate(() => {
      return document.readyState === 'complete';
    });

    return {
      pass: hasNoErrors && isLoaded,
      message: () =>
        hasNoErrors
          ? 'Page loaded with errors'
          : 'Page did not finish loading',
    };
  },

  toBeWithinRange(received, floor, ceiling) {
    const pass = received >= floor && received <= ceiling;
    return {
      pass,
      message: () =>
        `expected ${received} ${pass ? 'not ' : ''}to be within range ${floor} - ${ceiling}`,
    };
  },
});

// Declaraciones de tipos
declare global {
  namespace PlaywrightTest {
    interface Matchers<R> {
      toHaveLoadedSuccessfully(): Promise<R>;
    }
  }
}
```

---

## Patrones de Pruebas Asíncronas

### Esperar elementos

```typescript
// Preferido: usar findBy* (espera automáticamente)
const element = await screen.findByText('Loaded');

// Esperar a que aparezca un elemento
await waitFor(() => {
  expect(screen.getByText('Loaded')).toBeInTheDocument();
});

// Esperar a que un elemento desaparezca
await waitForElementToBeRemoved(() => screen.queryByText('Loading...'));

// Esperar con timeout personalizado
await waitFor(
  () => {
    expect(mockFn).toHaveBeenCalled();
  },
  { timeout: 5000 }
);
```

### Prueba de cambios de estado asíncronos

```typescript
// __tests__/components/AsyncButton.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AsyncButton } from '../../src/components/AsyncButton';

describe('AsyncButton', () => {
  it('shows loading state during async operation', async () => {
    const user = userEvent.setup();
    const onClickMock = jest.fn().mockImplementation(
      () => new Promise(resolve => setTimeout(resolve, 100))
    );

    render(<AsyncButton onClick={onClickMock}>Submit</AsyncButton>);

    // Estado inicial
    expect(screen.getByRole('button')).toHaveTextContent('Submit');
    expect(screen.getByRole('button')).not.toBeDisabled();

    // Clic y verificación del estado de carga
    await user.click(screen.getByRole('button'));
    expect(screen.getByRole('button')).toHaveTextContent('Loading...');
    expect(screen.getByRole('button')).toBeDisabled();

    // Esperar a que finalice
    await waitFor(() => {
      expect(screen.getByRole('button')).toHaveTextContent('Submit');
      expect(screen.getByRole('button')).not.toBeDisabled();
    });
  });
});
```

### Prueba de funciones con debounce/throttle

```typescript
// __tests__/components/SearchInput.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SearchInput } from '../../src/components/SearchInput';

// Usar temporizadores simulados (fake timers) para probar el debounce
jest.useFakeTimers();

describe('SearchInput', () => {
  it('debounces search calls', async () => {
    const user = userEvent.setup({ advanceTimers: jest.advanceTimersByTime });
    const onSearchMock = jest.fn();

    render(<SearchInput onSearch={onSearchMock} debounceMs={300} />);

    // Escribir rápidamente
    await user.type(screen.getByRole('textbox'), 'test');

    // Todavía no hay llamadas (debounce en curso)
    expect(onSearchMock).not.toHaveBeenCalled();

    // Avanzar los temporizadores más allá del umbral de debounce
    jest.advanceTimersByTime(300);

    // Ahora debería haberse llamado una vez con el valor final
    expect(onSearchMock).toHaveBeenCalledTimes(1);
    expect(onSearchMock).toHaveBeenCalledWith('test');
  });
});
```

### Patrones asíncronos de Playwright

```typescript
// e2e/async-patterns.spec.ts
import { test, expect } from '@playwright/test';

test('waits for API response', async ({ page }) => {
  // Esperar una respuesta específica
  const responsePromise = page.waitForResponse('/api/data');
  await page.click('button.load-data');
  const response = await responsePromise;
  expect(response.status()).toBe(200);
});

test('waits for navigation', async ({ page }) => {
  await page.goto('/');
  await Promise.all([
    page.waitForURL('/dashboard'),
    page.click('a.dashboard-link'),
  ]);
});

test('waits for network idle', async ({ page }) => {
  await page.goto('/', { waitUntil: 'networkidle' });
});

test('retries assertion until pass', async ({ page }) => {
  // Aserción con reintento automático
  await expect(page.locator('.counter')).toHaveText('10', { timeout: 5000 });
});
```

### Pasos nombrados con test.step() para evidencia legible

Cuando un spec E2E queda ligado a un caso del runbook y se graba como
evidencia (ver `../references/video_evidence_guide.md`), envolver cada
paso lógico en `test.step()` hace que el reporte HTML y el trace viewer
muestren puntos de referencia nombrados, en vez de un video/trace corrido
sin marcas:

```typescript
// e2e/login-TC-01.spec.ts
import { test, expect } from '@playwright/test';

test('TC-01 [critical] - Login con credenciales válidas', async ({ page }) => {
  await test.step('Abrir la página de login', async () => {
    await page.goto('/login');
  });

  await test.step('Completar credenciales', async () => {
    await page.getByLabel('Email').fill(process.env.QA_USER_EMAIL!);
    await page.getByLabel('Password').fill(process.env.QA_USER_PASSWORD!);
  });

  await test.step('Enviar y verificar redirección', async () => {
    await page.getByRole('button', { name: 'Sign in' }).click();
    await expect(page).toHaveURL('/dashboard');
  });
});
```

Nombrá cada paso por su intención ("Completar credenciales"), no por la
acción cruda ("fill inputs"). Combinado con `QA_SLOWMO_MS` en
`playwright.config.ts`, esto es lo que hace que un video de evidencia sea
revisable por una persona en vez de solo "técnicamente correcto".

---

## Guía de Snapshot Testing

### Cuándo usar snapshots

| Buenos casos de uso | Malos casos de uso |
|----------------|---------------|
| Componentes de UI estáticos | Contenido dinámico |
| Mensajes de error | Timestamps/IDs |
| Objetos de configuración | Árboles de componentes grandes |
| Datos serializables | Componentes interactivos |

### Snapshots de componentes

```typescript
// __tests__/components/Button.test.tsx
import { render } from '@testing-library/react';
import { Button } from '../../src/components/Button';

describe('Button snapshots', () => {
  it('renders primary variant', () => {
    const { container } = render(
      <Button variant="primary">Click me</Button>
    );
    expect(container.firstChild).toMatchSnapshot();
  });

  it('renders secondary variant', () => {
    const { container } = render(
      <Button variant="secondary">Click me</Button>
    );
    expect(container.firstChild).toMatchSnapshot();
  });

  it('renders disabled state', () => {
    const { container } = render(
      <Button disabled>Click me</Button>
    );
    expect(container.firstChild).toMatchSnapshot();
  });
});
```

### Snapshots inline

```typescript
// Adecuado para salidas pequeñas y estables
it('formats date correctly', () => {
  const result = formatDate(new Date('2024-01-15'));
  expect(result).toMatchInlineSnapshot(`"January 15, 2024"`);
});

it('generates expected error message', () => {
  const error = new ValidationError('email', 'Invalid format');
  expect(error.message).toMatchInlineSnapshot(
    `"Validation failed for 'email': Invalid format"`
  );
});
```

### Buenas prácticas de snapshots

1. **Mantené los snapshots pequeños**: capturá elementos específicos, no páginas completas
2. **Usá snapshots inline para salidas pequeñas**: son más fáciles de revisar en el código
3. **Revisá con atención los cambios de snapshot**: no los actualices a ciegas
4. **Evitá snapshots para contenido dinámico**: filtrá timestamps e IDs
5. **Combiná con otras aserciones**: los snapshots complementan, no reemplazan

```typescript
// Filtrar contenido dinámico de los snapshots
it('renders user card', () => {
  const { container } = render(<UserCard user={mockUser} />);

  // Eliminar elementos dinámicos antes del snapshot
  const card = container.firstChild;
  const timestamp = card.querySelector('.timestamp');
  timestamp?.remove();

  expect(card).toMatchSnapshot();
});
```

---

## Resumen

1. **Usá Page Objects** para interacciones de página complejas y reutilizables
2. **Construí factories** para la creación consistente de datos de prueba
3. **Aprovechá MSW** para un mocking de API realista
4. **Creá utilidades de render personalizadas** para el wrapping de providers
5. **Dominá los patrones asíncronos** para evitar pruebas inestables (flaky)
6. **Usá snapshots con criterio**, solo para contenido estable y estático
