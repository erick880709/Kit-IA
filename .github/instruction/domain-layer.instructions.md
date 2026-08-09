---
applyTo: "src/domain/**"
description: "Reglas para la capa de dominio: entidades puras e interfaces de repositorio"
---

# Instrucciones — Capa `src/domain/`

El dominio es el **núcleo de la aplicación**. No conoce ningún framework, ORM ni SDK de Azure.

## Entidades de Dominio (`src/domain/entities/`)

```typescript
// Correcto — clase TypeScript pura, sin decoradores ORM
export class OrderEntity {
  readonly id: string;
  readonly customerId: string;
  readonly createdAt: Date;

  constructor(props: { id?: string; customerId: string; createdAt?: Date }) {
    this.id = props.id ?? crypto.randomUUID();
    this.customerId = props.customerId;
    this.createdAt = props.createdAt ?? new Date();
  }
}
```

### Reglas para entidades

- **NUNCA** importar `typeorm`, `@azure/functions`, `pg` ni ningún SDK externo.
- Sin decoradores `@Entity`, `@Column`, etc. — eso pertenece a `infrastructure/`.
- El constructor debe aceptar un objeto de props tipado.
- Las propiedades deben ser `readonly` cuando sea posible.
- Usar `crypto.randomUUID()` para generar IDs por defecto.

## Interfaces de Repositorio (`src/domain/repositories/`)

```typescript
// Correcto — interfaz pura, retorna domain entities
export interface IOrderRepository {
  findById(id: string): Promise<OrderEntity | null>;
  findAll(): Promise<OrderEntity[]>;
  save(entity: OrderEntity): Promise<OrderEntity>;
  delete(id: string): Promise<void>;
}
```

### Reglas para interfaces de repositorio

- Nombre siempre con prefijo `I` + nombre de entidad + `Repository`.
- Los tipos de retorno usan **domain entities**, NO TypeORM entities.
- **NUNCA** importar tipos de TypeORM ni de ningún ORM en estas interfaces.
- Las implementaciones concretas viven en `src/infrastructure/database/repositories/`.
