---
applyTo: "src/functions/**"
description: "Reglas para archivos de registro de triggers Azure Functions v4 (model v4)"
---

# Instrucciones — Capa `src/functions/`

Esta capa **solo** registra triggers HTTP usando `app.http()` del paquete `@azure/functions`.
No debe contener lógica de negocio, validación ni acceso a datos.

## Patrón obligatorio

```typescript
import { app } from "@azure/functions";
import { <verb><Resource>Handler } from "../handlers/<verb>-<resource>.handler";

// Registro en ámbito global — NUNCA dentro de otra función
app.http("<verb><Resource>", {
  methods: ["<METHOD>"],
  authLevel: "anonymous",   // La auth la gestiona APIM + middleware JWT interno
  route: "<resources>",     // kebab-case, plural. Con parámetros: "orders/{id}"
  handler: <verb><Resource>Handler,
});
```

## Reglas

- Un archivo por endpoint.
- El nombre del registro (`app.http("nombre", ...)`) debe ser **camelCase** del verbo+recurso.
- La `route` NO debe incluir el prefijo `/api` — Azure Functions lo agrega automáticamente.
- `authLevel: "anonymous"` siempre — la autenticación ocurre dentro del handler vía middleware JWT.
- **NUNCA** uses `function.json` — pertenece al model v3.
- **NUNCA** exportes la función con la firma de model v3: `async function(context, req)`.
