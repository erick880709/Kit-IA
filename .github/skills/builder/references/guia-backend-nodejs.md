# Guía Senior: Backend Node.js / TypeScript

Patrones, anti-patrones y convenciones para scaffolds de backend Node.js con Express, Fastify y NestJS.

---

## Estructura de proyecto (Clean Architecture con Express/Fastify + TypeScript)

```
src/
├── domain/                          # Capa de dominio — sin imports de Express/Prisma
│   ├── entities/
│   │   └── <entidad>.ts             # Clase/interface de dominio pura
│   ├── value-objects/
│   │   └── <entidad>-id.ts
│   ├── ports/
│   │   ├── <entidad>-repository.ts  # Interfaz del repositorio
│   │   └── event-publisher.ts
│   └── exceptions.ts
├── application/                     # Casos de uso
│   ├── <entidad>/
│   │   ├── create-<entidad>.ts      # Comando (función o clase)
│   │   ├── get-<entidad>.ts         # Query
│   │   └── <entidad>-dto.ts         # Zod schemas de entrada/salida
│   └── common/
│       └── pagination.ts
├── infrastructure/                  # Adaptadores
│   ├── persistence/
│   │   ├── prisma/
│   │   │   └── schema.prisma
│   │   └── repositories/
│   │       └── prisma-<entidad>-repository.ts
│   ├── messaging/                   # Kafka, RabbitMQ, SQS
│   └── clients/                     # APIs externas
├── presentation/                    # Routers Express/Fastify
│   ├── <entidad>/
│   │   ├── <entidad>-router.ts      # Express Router
│   │   └── <entidad>-schemas.ts     # Zod schemas de request/response
│   ├── middleware/
│   │   ├── error-handler.ts
│   │   ├── auth.ts
│   │   └── request-id.ts
│   └── app.ts                       # Express/Fastify app factory
├── config/
│   └── env.ts                       # Zod-validated environment variables
└── index.ts                         # Entry point
```

## Reglas de diseño senior

### 1. Zod para TODO — validación en runtime, tipos en compile-time

**✅ Siempre:** schemas Zod para validar input, output, y variables de entorno. TypeScript solo da seguridad en compilación; Zod la da en runtime.

```typescript
import { z } from "zod";

// Schema de request (input validation)
export const CreateOrderSchema = z.object({
  customerId: z.string().uuid(),
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number().int().min(1).max(100),
  })).min(1).max(50),
  notes: z.string().max(500).optional(),
}).strict(); // Rechaza campos no declarados

// Schema de respuesta (output typing)
export const OrderResponseSchema = z.object({
  id: z.string().uuid(),
  customerId: z.string().uuid(),
  status: z.enum(["PENDING", "PAID", "SHIPPED", "DELIVERED", "CANCELLED"]),
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number(),
    unitPrice: z.number(),
  })),
  total: z.number(),
  createdAt: z.string().datetime(),
});

// Tipos inferidos (NO los escribas a mano)
export type CreateOrderInput = z.infer<typeof CreateOrderSchema>;
export type OrderResponse = z.infer<typeof OrderResponseSchema>;
```

### 2. Configuración validada con Zod

```typescript
// config/env.ts
import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "test", "production"]).default("development"),
  PORT: z.coerce.number().int().positive().default(3000),
  DATABASE_URL: z.string().url(),
  REDIS_URL: z.string().url().optional(),
  JWT_SECRET: z.string().min(32),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
});

export const env = envSchema.parse(process.env);
// Si alguna variable falta o es inválida, la app CRASHEA al arrancar — no en producción.
```

### 3. Prisma: schema como fuente de verdad

```prisma
// infrastructure/persistence/prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Order {
  id         String   @id @default(uuid()) @db.Uuid
  customerId String   @map("customer_id") @db.Uuid
  status     String   @default("PENDING") @db.VarChar(20)
  createdAt  DateTime @default(now()) @map("created_at")
  updatedAt  DateTime @updatedAt @map("updated_at")

  items      OrderItem[]
  customer   Customer  @relation(fields: [customerId], references: [id])

  @@map("orders")
}

model OrderItem {
  id        String  @id @default(uuid()) @db.Uuid
  orderId   String  @map("order_id") @db.Uuid
  productId String  @map("product_id") @db.Uuid
  quantity  Int
  unitPrice Decimal @map("unit_price") @db.Decimal(10, 2)

  order Order @relation(fields: [orderId], references: [id], onDelete: Cascade)

  @@map("order_items")
}
```

### 4. Repositorio: interfaz en dominio, implementación con Prisma

```typescript
// domain/ports/order-repository.ts
export interface OrderRepository {
  findById(id: string): Promise<Order | null>;
  save(order: Order): Promise<Order>;
  findAll(filter: OrderFilter): Promise<PaginatedResult<Order>>;
}

// infrastructure/persistence/repositories/prisma-order-repository.ts
import { PrismaClient } from "@prisma/client";

export class PrismaOrderRepository implements OrderRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async findById(id: string): Promise<Order | null> {
    const model = await this.prisma.order.findUnique({
      where: { id },
      include: { items: true },
    });
    return model ? this.toDomain(model) : null;
  }

  private toDomain(model: OrderModel): Order {
    return Order.reconstitute({
      id: model.id,
      customerId: model.customerId,
      status: model.status as OrderStatus,
      items: model.items.map(i => ({ productId: i.productId, quantity: i.quantity, unitPrice: Number(i.unitPrice) })),
    });
  }
}
```

### 5. Express: error handler centralizado (Express 5+)

```typescript
// presentation/middleware/error-handler.ts
import { Request, Response, NextFunction } from "express";
import { ZodError } from "zod";
import { DomainException, NotFoundException } from "../../domain/exceptions";

export function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  if (err instanceof ZodError) {
    res.status(400).json({
      error: "Validation Error",
      details: err.errors.map(e => ({ path: e.path.join("."), message: e.message })),
    });
    return;
  }

  if (err instanceof NotFoundException) {
    res.status(404).json({ error: err.message });
    return;
  }

  if (err instanceof DomainException) {
    res.status(422).json({ error: err.message });
    return;
  }

  console.error("Unhandled error:", err);
  res.status(500).json({ error: "Internal server error" });
}
```

### 6. Express router tipado con Zod

```typescript
// presentation/orders/order-router.ts
import { Router } from "express";
import { CreateOrderSchema } from "./order-schemas";

const router = Router();

router.post("/", async (req, res, next) => {
  try {
    const input = CreateOrderSchema.parse(req.body); // Valida y tipa
    const handler = new CreateOrderHandler(orderRepo);
    const result = await handler.execute(input);
    res.status(201).json(result);
  } catch (err) {
    next(err); // Delegar al error handler centralizado
  }
});
```

### 7. Testing — reglas de oro

| Tipo | Framework | Convención |
|---|---|---|
| **Unitario (dominio)** | Vitest / Jest | `test/unit/<entidad>.test.ts`. Sin DB. |
| **Integración (repo)** | Vitest + Testcontainers (PostgreSQL) | `test/integration/<entidad>-repository.test.ts`. |
| **API** | Supertest + Vitest | `test/api/<entidad>.test.ts`. |

```typescript
// test/unit/order.test.ts
import { describe, it, expect } from "vitest";
import { Order } from "@/domain/entities/order";

describe("Order", () => {
  it("should change status to PAID when markAsPaid is called on a PENDING order", () => {
    const order = Order.create({ customerId: "uuid", items: [...] });
    order.markAsPaid();
    expect(order.status).toBe("PAID");
  });

  it("should throw when marking as shipped a non-paid order", () => {
    const order = Order.create({ customerId: "uuid", items: [...] });
    expect(() => order.markAsShipped()).toThrow("pagada");
  });
});
```

## Stack recomendado por defecto (greenfield)

| Rol | Tecnología | Alternativa |
|---|---|---|
| Runtime | Node.js 22 LTS | Bun |
| Lenguaje | TypeScript 5.x (strict) | — |
| Framework | Express 5 / Fastify 5 | NestJS (si equipo grande, ama decoradores) |
| ORM | Prisma | Drizzle (si SQL raw necesario) |
| Validación | Zod | Valibot (más ligero) |
| Testing | Vitest + Supertest | Jest |
| Logging | pino | winston |
| Observabilidad | OpenTelemetry + pino | — |
| Container | `node:22-alpine` | Distroless |
