# Guía Senior: Frontend Angular

Patrones, anti-patrones y convenciones para scaffolds de frontend Angular 17+ (standalone components, signals, control flow syntax). Aplica a proyectos greenfield y nuevos módulos.

---

## Estructura de proyecto (Angular 18+ standalone)

```
src/app/
├── core/                            # Singleton services, guards, interceptors
│   ├── guards/
│   │   └── auth.guard.ts
│   ├── interceptors/
│   │   ├── auth.interceptor.ts      # Agrega token JWT a cada request
│   │   └── error.interceptor.ts     # Manejo global de errores HTTP
│   ├── services/
│   │   └── auth.service.ts
│   └── core.module.ts               # (solo si no es 100% standalone. Preferir `providedIn: 'root'`)
├── shared/                          # Componentes, pipes, directivas reutilizables
│   ├── components/
│   │   ├── confirm-dialog/
│   │   ├── data-table/              # Tabla genérica con sort, filter, pagination
│   │   └── loading-spinner/
│   ├── directives/
│   └── pipes/
├── features/                        # Módulos de dominio (lazy-loaded)
│   └── <entidad>/
│       ├── pages/                   # Componentes de ruta (smart components)
│       │   ├── <entidad>-list/
│       │   │   ├── <entidad>-list.component.ts
│       │   │   └── <entidad>-list.component.html
│       │   ├── <entidad>-detail/
│       │   └── <entidad>-form/
│       ├── components/              # Componentes dumb específicos del feature
│       │   ├── <entidad>-card/
│       │   └── <entidad>-filter/
│       ├── services/
│       │   └── <entidad>.service.ts
│       ├── models/
│       │   └── <entidad>.model.ts   # Interfaces/types
│       └── routes.ts                # Configuración de rutas (lazy)
├── app.config.ts                    # provideHttpClient, provideRouter, etc.
├── app.routes.ts                    # Rutas raíz con lazy loading
└── app.component.ts
```

## Reglas de diseño senior

### 1. Standalone components — NO NgModules

**✅ Siempre:** standalone components, pipes, directives. NgModules son legacy desde Angular 17.

```typescript
// order-list.component.ts
import { Component, inject, signal } from "@angular/core";
import { AsyncPipe } from "@angular/common";
import { RouterLink } from "@angular/router";
import { OrderService } from "../services/order.service";
import { DataTableComponent } from "../../../shared/components/data-table/data-table.component";

@Component({
  selector: "app-order-list",
  standalone: true,
  imports: [AsyncPipe, RouterLink, DataTableComponent],
  templateUrl: "./order-list.component.html",
})
export class OrderListComponent {
  private readonly orderService = inject(OrderService);

  orders = this.orderService.orders;  // Signal o Observable del servicio
  loading = this.orderService.loading;

  constructor() {
    this.orderService.loadAll();
  }
}
```

### 2. Signals para estado reactivo (Angular 17+)

**✅ Siempre:** signals en componentes. Services pueden usar signals o RxJS según complejidad.

```typescript
// order.service.ts
import { Injectable, signal, inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { lastValueFrom } from "rxjs";

@Injectable({ providedIn: "root" })
export class OrderService {
  private readonly http = inject(HttpClient);

  readonly orders = signal<Order[]>([]);
  readonly loading = signal(false);
  readonly error = signal<string | null>(null);

  async loadAll(): Promise<void> {
    this.loading.set(true);
    this.error.set(null);
    try {
      const data = await lastValueFrom(
        this.http.get<OrderResponse[]>("/api/orders")
      );
      this.orders.set(data);
    } catch (err) {
      this.error.set("Error al cargar órdenes");
    } finally {
      this.loading.set(false);
    }
  }

  async create(input: CreateOrderInput): Promise<OrderResponse> {
    const created = await lastValueFrom(
      this.http.post<OrderResponse>("/api/orders", input)
    );
    this.orders.update(list => [...list, created]);
    return created;
  }
}
```

### 3. Control flow syntax (@if, @for, @switch)

**✅ Siempre:** nueva sintaxis de control flow (Angular 17+). NO usar `*ngIf`, `*ngFor`, `*ngSwitch`.

```html
<!-- order-list.component.html -->
@if (loading()) {
  <app-loading-spinner />
} @else if (error()) {
  <div class="alert alert-error">{{ error() }}</div>
} @else {
  <app-data-table [data]="orders()" [columns]="columns">
    @for (order of orders(); track order.id) {
      <tr>
        <td>{{ order.id | slice:0:8 }}</td>
        <td>{{ order.customerId }}</td>
        <td>
          <span [class]="'badge badge-' + order.status">
            {{ order.status | titlecase }}
          </span>
        </td>
        <td>{{ order.total | currency }}</td>
        <td>{{ order.createdAt | date:'short' }}</td>
        <td>
          <a [routerLink]="[order.id]">Ver</a>
        </td>
      </tr>
    } @empty {
      <tr><td [colSpan]="6">No se encontraron órdenes</td></tr>
    }
  </app-data-table>
}
```

### 4. Formularios reactivos tipados (Angular 14+)

```typescript
// order-form.component.ts
import { Component, inject, input, output } from "@angular/core";
import { FormBuilder, ReactiveFormsModule, Validators } from "@angular/forms";

interface OrderForm {
  customerId: FormControl<string>;
  notes: FormControl<string | null>;
}

@Component({
  selector: "app-order-form",
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: "./order-form.component.html",
})
export class OrderFormComponent {
  private readonly fb = inject(FormBuilder).nonNullable;

  readonly orderId = input<string>();
  readonly saved = output<OrderResponse>();

  form = this.fb.group<OrderForm>({
    customerId: this.fb.control("", [Validators.required, Validators.minLength(3)]),
    notes: this.fb.control(null),
  });

  async onSubmit(): Promise<void> {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    // this.form.value es tipado: { customerId: string; notes: string | null }
    const result = await this.orderService.create(this.form.getRawValue());
    this.saved.emit(result);
  }
}
```

### 5. HttpClient interceptor para auth

```typescript
// core/interceptors/auth.interceptor.ts
import { HttpInterceptorFn } from "@angular/common/http";
import { inject } from "@angular/core";
import { AuthService } from "../services/auth.service";

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const auth = inject(AuthService);
  const token = auth.token();

  if (token && !req.url.includes("/auth/")) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` },
    });
  }
  return next(req);
};

// app.config.ts — registrar el interceptor
export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(withInterceptors([authInterceptor, errorInterceptor])),
    provideRouter(routes),
  ],
};
```

### 6. Lazy loading de features

```typescript
// app.routes.ts
import { Routes } from "@angular/router";

export const routes: Routes = [
  {
    path: "orders",
    loadChildren: () =>
      import("./features/orders/routes").then((m) => m.ORDER_ROUTES),
  },
  {
    path: "products",
    loadChildren: () =>
      import("./features/products/routes").then((m) => m.PRODUCT_ROUTES),
  },
  { path: "", redirectTo: "/orders", pathMatch: "full" },
  { path: "**", redirectTo: "/orders" },
];
```

### 7. Modelos con interfaces tipadas

```typescript
// features/orders/models/order.model.ts
export interface OrderResponse {
  id: string;
  customerId: string;
  status: OrderStatus;
  items: OrderItemResponse[];
  total: number;
  createdAt: string;
}

export interface CreateOrderInput {
  customerId: string;
  items: { productId: string; quantity: number }[];
  notes?: string;
}

export type OrderStatus = "PENDING" | "PAID" | "SHIPPED" | "DELIVERED" | "CANCELLED";
```

### 8. Testing — reglas de oro

| Tipo | Framework | Convención |
|---|---|---|
| **Unitario (service)** | Jasmine / Jest | `order.service.spec.ts`. Mockear HttpClient. |
| **Componente** | TestBed + Jasmine/Jest | `order-list.component.spec.ts`. Shallow render. |
| **Integración** | TestBed con HttpClientTestingModule | `order-create-flow.spec.ts`. |

```typescript
// order.service.spec.ts
describe("OrderService", () => {
  let service: OrderService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [provideHttpClient(), provideHttpClientTesting()],
    });
    service = TestBed.inject(OrderService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it("should load orders and update signal", async () => {
    const mockOrders: OrderResponse[] = [{ id: "1", ... }];

    service.loadAll();
    const req = httpMock.expectOne("/api/orders");
    req.flush(mockOrders);

    expect(service.orders()).toEqual(mockOrders);
    expect(service.loading()).toBeFalse();
  });
});
```

## Stack recomendado por defecto (greenfield Angular)

| Rol | Tecnología | Versión |
|---|---|---|
| Framework | Angular | 18+ |
| Lenguaje | TypeScript | 5.5+ (strict) |
| UI Components | Angular Material / Taiga UI | Latest |
| Estilos | Tailwind CSS (recomendado) / SCSS | — |
| Estado global | Signals (built-in) / NgRx SignalStore | — |
| Formularios | Reactive Forms (typed) | — |
| HTTP | HttpClient + interceptors funcionales | — |
| Testing | Jasmine + Karma / Jest | — |
| Build | esbuild (Angular CLI `@angular/build`) | — |
| Linting | ESLint + angular-eslint + prettier | — |
| Container | nginx:alpine (multi-stage build) | — |
