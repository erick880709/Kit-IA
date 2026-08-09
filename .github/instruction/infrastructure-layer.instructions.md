---
applyTo: "src/infrastructure/**"
description: "Reglas para TypeORM entities, repositorios concretos, Key Vault y DataSource"
---

# Instrucciones — Capa `src/infrastructure/`

Esta capa contiene las implementaciones concretas que dependen de tecnologías externas.

## TypeORM Entities (`src/infrastructure/database/entities/`)

```typescript
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn } from "typeorm";

// Separada de la domain entity — solo conoce la persistencia
@Entity("orders")
export class OrderTypeOrmEntity {
  @PrimaryGeneratedColumn("uuid")
  id: string;

  @Column({ name: "customer_id" })
  customerId: string;

  @CreateDateColumn({ name: "created_at" })
  createdAt: Date;

  @UpdateDateColumn({ name: "updated_at" })
  updatedAt: Date;
}
```

## Repositorios TypeORM (`src/infrastructure/database/repositories/`)

```typescript
import { DataSource, Repository } from "typeorm";
import { IOrderRepository } from "../../../domain/repositories/i-order.repository";
import { OrderEntity } from "../../../domain/entities/order.entity";
import { OrderTypeOrmEntity } from "../entities/order.typeorm-entity";

export class TypeOrmOrderRepository implements IOrderRepository {
  private readonly repo: Repository<OrderTypeOrmEntity>;

  constructor(dataSource: DataSource) {
    this.repo = dataSource.getRepository(OrderTypeOrmEntity);
  }

  async findById(id: string): Promise<OrderEntity | null> {
    const record = await this.repo.findOne({ where: { id } });
    return record ? this.toDomain(record) : null;
  }

  async save(entity: OrderEntity): Promise<OrderEntity> {
    const saved = await this.repo.save(this.toOrm(entity));
    return this.toDomain(saved);
  }

  // Mappers privados — SIEMPRE incluirlos
  private toDomain(r: OrderTypeOrmEntity): OrderEntity {
    return new OrderEntity({ id: r.id, customerId: r.customerId, createdAt: r.createdAt });
  }

  private toOrm(e: OrderEntity): Partial<OrderTypeOrmEntity> {
    return { id: e.id, customerId: e.customerId };
  }
}
```

## Reglas

- `synchronize: true` **SOLO** en tests (`NODE_ENV === "test"`). **Nunca** en producción.
- El `DataSource` debe ser **singleton** — usar `getDataSource()` de `data-source.ts`.
- Todos los cambios de esquema en producción deben hacerse con `migrations/`.
- SSL habilitado en producción: `ssl: { rejectUnauthorized: true }`.
- Usar `DefaultAzureCredential` para Key Vault — **nunca** hardcodear credenciales.
- El nombre del archivo TypeORM entity: `<resource>.typeorm-entity.ts`.
- El nombre del repositorio concreto: `typeorm-<resource>.repository.ts`.
