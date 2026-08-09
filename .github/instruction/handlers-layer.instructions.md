---
applyTo: "src/handlers/**"
description: "Reglas para la capa de handlers: validación de input y mapeo de errores HTTP"
---

# Instrucciones — Capa `src/handlers/`

Los handlers son la **capa de presentación**. Reciben la `HttpRequest`, validan el input,
llaman al use case correspondiente y mapean el resultado a `HttpResponseInit`.

## Firma obligatoria

```typescript
import { HttpRequest, HttpResponseInit, InvocationContext } from "@azure/functions";

export async function <verb><Resource>Handler(
  request: HttpRequest,
  context: InvocationContext
): Promise<HttpResponseInit> { ... }
```

## Responsabilidades del handler

1. **Verificar autenticación** con `verifyJwt(request)` (si el endpoint lo requiere).
2. **Extraer y validar** el body / path params / query params.
3. **Instanciar dependencias** (Composition Root a nivel de invocación).
4. **Llamar al use case** y obtener el resultado.
5. **Retornar `HttpResponseInit`** con el status y body apropiados.
6. **Capturar errores** y delegarlos a `mapDomainErrorToHttp(error, context)`.

## Reglas

- **NO** importar clases de `infrastructure/` directamente para lógica de negocio.
- **NO** acceder a la base de datos directamente — siempre a través del use case.
- **SIEMPRE** usar `try/catch` y `mapDomainErrorToHttp` para errores no controlados.
- Los errores de dominio (`NotFoundError`, `ValidationError`, etc.) se mapean en `shared/errors/error-mapper.ts`.
- El `DataSource` se obtiene con `getDataSource()` del singleton de infraestructura.

## Ejemplo de estructura

```typescript
export async function createOrderHandler(
  request: HttpRequest,
  context: InvocationContext
): Promise<HttpResponseInit> {
  try {
    // 1. Autenticación
    const claims = await verifyJwt(request);

    // 2. Extraer input
    const body = await request.json() as CreateOrderDto;

    // 3. Instanciar dependencias (Composition Root)
    const dataSource = await getDataSource();
    const orderRepo = new TypeOrmOrderRepository(dataSource);
    const useCase = new CreateOrderUseCase(orderRepo);

    // 4. Ejecutar caso de uso
    const result = await useCase.execute(body);

    // 5. Retornar respuesta HTTP
    return { status: 201, jsonBody: result };

  } catch (error) {
    return mapDomainErrorToHttp(error, context);
  }
}
```
